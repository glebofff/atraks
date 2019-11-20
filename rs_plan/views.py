from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    return render(
        request=request,
        template_name='rs_plan/index.html'
    )


class CheckView(TemplateView):
    def get(self, request, *args, number=None, **kwargs):
        from django.http import JsonResponse
        result = {
            'ok': True,
            'statusText': '',
            'number': f'{number}',
            'org': None,
            'reg': None
        }
        try:
            from rs_plan.utils.msdisdn import MSISDN
            num = MSISDN.parse(number)
            result['number'] = num.number
            plan = num.plan

            if not plan:
                raise Exception(f'No record found for number: {number}')

            result['org'] = plan.operator.name if plan.operator else 'n/a'
            result['reg'] = plan.region.name if plan.region else 'n/a'

        except Exception as e:
            result['ok'] = False
            result['statusText'] = f'{e}'

        return JsonResponse(result)

