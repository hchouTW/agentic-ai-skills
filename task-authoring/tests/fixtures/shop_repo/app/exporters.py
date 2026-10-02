class ExporterFactory:
    _registry = {}

    @classmethod
    def register(cls, name):
        def deco(klass):
            cls._registry[name] = klass
            return klass
        return deco

    @classmethod
    def create(cls, name):
        return cls._registry[name]()


@ExporterFactory.register("csv")
class CsvExporter:
    def export(self, rows):
        return "\n".join(",".join(map(str, r)) for r in rows)
