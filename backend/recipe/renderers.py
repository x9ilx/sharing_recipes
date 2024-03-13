from rest_framework import renderers


class SubscribeRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        result = []
        try:
            if renderer_context['request'].method == 'GET':
                for item in data['results']:
                    item['author']['recipes'] = item['recipes']
                    item['author']['recipes_count'] = item['recipes_count']
                    result.append(item['author'])

                data['results'] = result
            else:
                author = data.pop('author')
                data.update(**author)

            return super(SubscribeRenderer, self).render(
                data, accepted_media_type, renderer_context
            )

        except Exception as ex:
            data = {
                'detail': data,
            }

        return super(SubscribeRenderer, self).render(
            data, accepted_media_type, renderer_context
        )

    def get_default_renderer(self, view):
        return renderers.JSONRenderer()
