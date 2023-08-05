import aiohttp
from tracardi.service.storage.helpers.source_reader import read_source
from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result
from tracardi_text_classification.model.configuration import Configuration
from tracardi_text_classification.model.ml_source_onfiguration import MLSourceConfiguration


class TextClassificationAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'TextClassificationAction':
        plugin = TextClassificationAction(**kwargs)
        source = await read_source(plugin.config.source.id)
        plugin.source = MLSourceConfiguration(
            **source.config
        )

        return plugin

    def __init__(self, **kwargs):
        self.source = None
        self.config = Configuration(**kwargs)
        self.models = {
            'social': 'SocialMedia_en',
            'press': 'IPTC_en'
        }

    async def run(self, payload):

        if self.config.model not in self.models:
            raise ValueError(f"Model `{self.config.model}` is incorrect. Available models are `{self.models}`")

        dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)

        async with aiohttp.ClientSession() as session:
            params = {
                "key": self.source.token,
                "lang": self.config.language,
                "txt": dot[self.config.text],
                "model": self.models[self.config.model]
            }

            if self.config.has_title():
                params['title'] = dot[self.config.title]

            try:
                async with session.post('https://api.meaningcloud.com/class-2.0', params=params) as response:
                    if response.status != 200:
                        raise ConnectionError("Could not connect to service https://api.meaningcloud.com. "
                                              f"It returned `{response.status}` status.")

                    data = await response.json()
                    if 'status' in data and 'msg' in data['status']:
                        if data['status']['msg'] != "OK":
                            raise ValueError(data['status']['msg'])

                    result = {
                        "categories": data['category_list'],
                    }

                    return Result(port="payload", value=result), Result(port="error", value=None)

            except Exception as e:
                self.console.error(repr(e))
                return Result(port="payload", value=None), Result(port="error", value=str(e))


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_text_classification.plugin',
            className='TextClassificationAction',
            inputs=["payload"],
            outputs=['payload', 'error'],
            version='0.1',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "source": {
                    "id": None
                },
                "language": "en",
                "model": "social",
                "title": None,
                "text": None
            }
        ),
        metadata=MetaData(
            name='Text classification',
            desc='It connects to the service that classifies a given sentence.',
            type='flowNode',
            width=200,
            height=100,
            icon='paragraph',
            group=["Machine learning"]
        )
    )
