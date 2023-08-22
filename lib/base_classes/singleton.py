class SingletonMetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance.keys():
            cls._instance[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instance[cls]
