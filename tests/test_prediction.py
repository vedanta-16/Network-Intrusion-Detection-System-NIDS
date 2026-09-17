def test_prediction_module_imports():
    from src.predict import predict_traffic
    assert callable(predict_traffic)
