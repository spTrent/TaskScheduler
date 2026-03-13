from .contracts.source import Source
from .sources import (
    api_source,
    file_source,
    generator_source,
    json_source
)

sources = [api_source.ApiMock(), file_source.FileSource('test.txt'), generator_source.GeneratorSource(), json_source.JsonSource('test.json')]
for source in sources:
    print(f'isinstance({source}, Source): {isinstance(source, Source)}')