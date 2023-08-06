from hestia_earth.schema import TermTermType
from hestia_earth.utils.tools import safe_parse_float
from hestia_earth.utils.model import filter_list_term_type, find_primary_product

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.crop import get_crop_lookup_value
from .. import MODEL

MODEL_KEY = 'economicValueShare'


def _product(product: dict, value: float):
    logger.info('model=%s, key=%s, value=%s, term=%s', MODEL, MODEL_KEY, value, product.get('term', {}).get('@id'))
    return {**product, MODEL_KEY: value}


def _run_by_revenue(products: list):
    total_revenue = sum([p.get('revenue', 0) for p in products])
    return [_product(p, p.get('revenue', 0) / total_revenue * 100) for p in products if p.get('revenue') > 0]


def _run_by_crop(product: dict):
    term = product.get('term', {}).get('@id')
    value = safe_parse_float(get_crop_lookup_value(term, 'global_economic_value_share'), None)
    return [] if value is None else [_product(product, value)]


def _should_run_by_crop(cycle: dict):
    primary_product = find_primary_product(cycle) or {}
    product_is_crop = primary_product.get('term', {}).get('termType') == TermTermType.CROP.value
    single_product_crop = len(filter_list_term_type(cycle.get('products', []), TermTermType.CROP)) == 1

    debugRequirements(model=MODEL, term=MODEL_KEY,
                      product_is_crop=product_is_crop,
                      single_product_crop=single_product_crop)

    should_run = all([product_is_crop, single_product_crop])
    logger.info('model=%s, key=%s, should_run=%s', MODEL, MODEL_KEY, should_run)
    return should_run


def _should_run_by_revenue(cycle: dict):
    products = cycle.get('products', [])
    total_value = sum([p.get(MODEL_KEY, 0) for p in products])
    all_with_revenue = all([p.get('revenue', 0) > 0 for p in products])

    debugRequirements(model=MODEL, term=MODEL_KEY,
                      total_value=total_value,
                      all_with_revenue=all_with_revenue)

    should_run = all([total_value < 100.5, all_with_revenue])
    logger.info('model=%s, key=%s, should_run_by_revenue=%s', MODEL, MODEL_KEY, should_run)
    return should_run


def run(cycle: dict):
    return _run_by_revenue(cycle.get('products', [])) if _should_run_by_revenue(cycle) else (
        _run_by_crop(find_primary_product(cycle)) if _should_run_by_crop(cycle) else []
    )
