from pricing import PricingService


def test_pricing_calculation():
    service = PricingService(base_rate=2.0)
    result = service.calculate_cost(10)
    assert result == 20.0


def test_pricing_zero_minutes():
    service = PricingService(base_rate=2.0)
    result = service.calculate_cost(0)
    assert result == 0.0


def test_pricing_negative_minutes():
    service = PricingService(base_rate=1.5)
    result = service.calculate_cost(-5)
    assert result == 0.0


def test_pricing_default_rate():
    service = PricingService()
    result = service.calculate_cost(10)
    assert result == 10.0