from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import AdcancedSearchFormSet,SELECT_FIELD_CHOICES,CONDITION_CHOICES
from django.conf import settings
from django.http import HttpResponse, request
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import get_collection_handle, get_db_handle, special_characters, count_categories, get_data_from_mongo, get_sample_data
class HomePageView(TemplateView):
    template_name = "rice/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db, _ = get_db_handle(settings.DB_NAME, settings.HOST_MONGODB)
        collection = get_collection_handle(db, settings.COLLECTION_NAME)
        cursor = collection.find()
        list_cur = list(cursor)
        rice_categories_count = count_categories(list_cur)
        context['rice_categories_count'] = rice_categories_count
        return context

class DocsPageView(TemplateView):
    template_name = "rice/docs.html"

def render_pdf_view(request):
    template_path = 'rice/pdf.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html.encode('utf-8'), dest=response,)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def rice_list_view(request):
    db, _ = get_db_handle(settings.DB_NAME, settings.HOST_MONGODB)
    collection = get_collection_handle(db, settings.COLLECTION_NAME)
    cursor = collection.find()
    if request.method == 'GET':
        search_form = request.GET.get('search-form', None)
        fiter_form = request.GET.get('fiter-form', None)
        sample_list = list()
        if search_form == 'home':
            query = request.GET.get('q', None)
            if query != None:
                query = special_characters(query)
            else:
                query = ''

            cursor = collection.find({'$or':[
                {"Sampleinfo.riceVarietiesEN": {'$regex': query} },
                {"Sampleinfo.riceVarietiesTH": {'$regex': query} },
                {"Sampleinfo.cropSiteProvince": {'$regex': query} },
                {"Sampleinfo.yearOfAnalysis": {'$regex': query} },
                {"Sampleinfo.siteOfAnalysis": {'$regex': query} },
                {"Sampleinfo.dataSource": {'$regex': query} }
                ]})
            list_cur = list(cursor)
            rice_categories_count = count_categories(list_cur)

            for item in list_cur:
                sample_list.append(item['Sampleinfo'])
            context = {'result':sample_list, 'rice_categories_count':rice_categories_count, 'q_serach':query}
        elif fiter_form != None:
            categories = {
            'Paddy rice':'ข้าวเปลือก',
            'Unmilled rice':'ข้าวกล้อง',
            'Milled rice':'ข้าวสาร',
            'Parboiled rice':'ข้าวนึ่ง',
            'Germinated rice':'ข้าวกล้องงอก',
            'Milk-stage rice':'ข้าวเม่า',
            'Cooked white rice':'ข้าวขาวสุก'
            }
            query = request.GET.get('q', None)
            select_field = request.GET.getlist('select_field', None)
            riceCat = [{'Physical.riceCategories' : categories[i] } for i in select_field]
            if riceCat and query:
                cursor = collection.find({'$and':[{ '$and': riceCat },
                {'$or':[
                    {"Sampleinfo.riceVarietiesEN": {'$regex': query} },
                    {"Sampleinfo.riceVarietiesTH": {'$regex': query} },
                    {"Sampleinfo.cropSiteProvince": {'$regex': query} },
                    {"Sampleinfo.yearOfAnalysis": {'$regex': query} },
                    {"Sampleinfo.siteOfAnalysis": {'$regex': query} },
                    {"Sampleinfo.dataSource": {'$regex': query} }
                ]}]})
            elif query:
                cursor = collection.find({'$or':[
                {"Sampleinfo.riceVarietiesEN": {'$regex': query} },
                {"Sampleinfo.riceVarietiesTH": {'$regex': query} },
                {"Sampleinfo.cropSiteProvince": {'$regex': query} },
                {"Sampleinfo.yearOfAnalysis": {'$regex': query} },
                {"Sampleinfo.siteOfAnalysis": {'$regex': query} },
                {"Sampleinfo.dataSource": {'$regex': query} }
                ]})
            elif riceCat:
                cursor = collection.find({ '$and': riceCat })
            else:
                cursor = collection.find()
            list_cur = list(cursor)
            rice_categories_count = count_categories(list_cur)

            for item in list_cur:
                sample_list.append(item['Sampleinfo'])
            context = {'result':sample_list, 'rice_categories_count':rice_categories_count, 'select_field':select_field, 'q_serach':query}
        else:
            cursor = collection.find()
            list_cur = list(cursor)
            rice_categories_count = count_categories(list_cur)

            for item in list_cur:
                sample_list.append(item['Sampleinfo'])
            context = {'result':sample_list, 'rice_categories_count':rice_categories_count}
    else:
        formset = AdcancedSearchFormSet(request.POST)
        if formset.is_valid():
            coll = {'riceVarietiesTH':'Sampleinfo', 'riceVarietiesEN':'Sampleinfo', 'cropSiteProvince':'Sampleinfo',
            'yearOfAnalysis':'Sampleinfo', 'siteOfAnalysis':'Sampleinfo', 'dataSource':'Sampleinfo', 'riceCategories':'Physical',
            'length':'Physical', 'color':'Physical', 'chalkiness':'Physical', 'amylose':'Chemical', 'content2AP':'Chemical',
            'carbohydrate':'Nutrition', 'protein':'Nutrition', 'totalFat':'Nutrition'}
            cond = {'eq':'$eq', 'gt':'$gt', 'lt':'$lt', 'ct':'$regex', 'bw':'$regex', 'ew':'$regex', 'ne':'$ne'}
            advanced_search = []
            queryOp1 = []
            queryOp2 = []
            for form in formset:
                select_field = form.cleaned_data.get('select_field')
                condition = form.cleaned_data.get('Condition')
                keyword = form.cleaned_data.get('Keyword')
                operation = form.cleaned_data.get('operation')
                advanced_search.append(
                    {
                    'select_field':dict(SELECT_FIELD_CHOICES).get(select_field),
                    'condition':dict(CONDITION_CHOICES).get(condition),
                    'keyword':keyword,
                    'operation':operation
                    })
                if condition == 'ct':
                    keyword = special_characters(keyword)
                    query = {f'{coll[select_field]}.{select_field}': {cond[condition]: f'{keyword}'}}
                elif condition == 'bw':
                    keyword = special_characters(keyword)
                    query = {f'{coll[select_field]}.{select_field}': {cond[condition]: f'^{keyword}'}}
                elif condition == 'ew':
                    keyword = special_characters(keyword)
                    query = {f'{coll[select_field]}.{select_field}': {cond[condition]: f'{keyword}$'}}
                else:
                    query = {f'{coll[select_field]}.{select_field}': {cond[condition]: keyword}}

                if operation == 'and':
                    queryOp1.append(query)
                else:
                    queryOp2.append(query)

            if len(queryOp2) == 0 :
                cursor = collection.find({'$and': queryOp1})
            elif len(queryOp1) == 0 :
                cursor = collection.find()

            else:
                qs = [{'$and': queryOp1}]
                qs.extend(queryOp2)
                cursor = collection.find({'$or': qs})
            list_cur = list(cursor)
            rice_categories_count = count_categories(list_cur)
            sample_list = list()
            for item in list_cur:
                sample_list.append(item['Sampleinfo'])
            context = {'result':sample_list, 'rice_categories_count':rice_categories_count,'advanced_search':advanced_search}
        else:
            return redirect('rice:advanced-search')
    return render(request, 'rice/results.html', context)

def get_data_name(request):
    if request.is_ajax():
        db, _ = get_db_handle(settings.DB_NAME, settings.HOST_MONGODB)
        collection = get_collection_handle(db, settings.COLLECTION_NAME)
        cursor = collection.find()
        data = []
        for item in list(cursor):
            data.append(item['Sampleinfo']['riceVarietiesTH'])
            data.append(item['Sampleinfo']['riceVarietiesEN'])

        data = list(set(data))
        return JsonResponse({'data':data})
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })

def get_data_info(request, pk, fieldGroup):

    list_item = get_data_from_mongo(pk, fieldGroup)

    return JsonResponse(list_item, safe=False)
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })

def info_view(request, pk):
    Sampleinfo = get_sample_data(pk)
    context = {'id': pk, 'prev':pk-1,'next':pk+1, 'riceVarieties':Sampleinfo[0]['Rice varieties'],'Sampleinfo': Sampleinfo[0]}
    return render(request, 'rice/info.html',context)


def advanced_search_view(request):
    template_name = 'rice/advanced_search.html'
    if request.method == 'GET':
        formset = AdcancedSearchFormSet(request.GET or None)
    return render(request, template_name, {
        'formset': formset
    })

def comparison_view(request):
    template_name = 'rice/compare.html'
    return render(request, template_name, {})

def get_data_comparison_view(request,fieldGroup):
    if request.is_ajax():
        if fieldGroup == 'Bioactive' and request.user.is_anonymous:
            return JsonResponse({'anonymous': True})
        else:
            fileldCase = {'Sampleinfo': 'Sample info','Physical': 'Physical properties', 'Chemical': 'Chemical properties', 'Nutrition': 'Nutrition', 'Bioactive': 'Bioactive compounds'}
            q = request.GET or None
            csid = q.getlist('csid')
            db, _ = get_db_handle(settings.DB_NAME, settings.HOST_MONGODB )
            collection = get_collection_handle(db, settings.COLLECTION_NAME)
            collection_meta = get_collection_handle(db, settings.COLLECTION_NAME_META)
            meta_data = collection_meta.find({"fieldGroup":fileldCase[fieldGroup]})
            meta = list()
            units = dict()
            meta.append('Nutrition DB ID')
            meta.append('Crop Sample ID')

            for item in meta_data:
                meta.append(item['fieldNameUIEN'])
                units[item['fieldNameDataFile']] = item['units']
            csid = list(map(int, csid))
            qs = [{'cropSampleID' : i } for i in csid]
            cursor = collection.find({'$or': qs})

            list_cur = list(cursor)
            sample = list()
            physical = list()
            fg = list()

            for item in list_cur:
                sample.append(item['Sampleinfo'])
                physical.append(item['Physical'])
                fg.append(item[fieldGroup])


            data = list()
            count = 0
            fieldName = dict()
            fieldUnits = dict()
            fieldName['riceVarietiesEN'] = 'Rice varieties'
            fieldName['riceCategories'] = 'Rice categories'
            for item_phy, item_fg in zip(physical, fg):
                for p, y in zip(item_phy, item_fg):
                    categories = dict()
                    for (key, value), name in zip(y.items(),meta):
                        if value:
                            categories[key] = value
                            if key not in fieldName:
                                fieldName[key] = " ".join(name.split())
                                if key in units :
                                    if units[key]:
                                        fieldUnits[key] = units[key]
                    if categories:
                        categories['riceCategories'] = p['riceCategories']
                        categories['riceVarietiesEN'] = sample[count]['riceVarietiesEN']
                        data.append(categories)
                count += 1
            return JsonResponse({'data':data, 'fieldName':fieldName, 'fieldUnits':fieldUnits}, safe=False)

    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })

class AboutPageView(TemplateView):
    template_name = "rice/about.html"
