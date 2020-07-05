from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer,ProductSerializer
from file_app.vgg16 import predict
from semantics3 import Products

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      file = file_serializer.data['file']
      print(file)

      #print(predict(file))
      result=predict(file)
      return Response({"file":file_serializer.data,"result":result}, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()

            upc = product_serializer.data['upc']
            ean = product_serializer.data['ean']

            sem3 = Products(
            api_key = "SEM358802643C8595EA80A4BA5F74DB35FD9",
            api_secret = "ZDhkMDJiNmEzMzdlMzVmZmQwNmNmZGVhODE4ZjQ4ZGQ"
            )


            if ean or len(ean)>5:
                print("EAN in")
                sem3.products_field("ean", ean)
            elif upc or len(upc)>5:
                print("UPC in")
                sem3.products_field("upc", upc)
            sem3.products_field("fields", ["name","gtins"])

            p = "product not found"
            # Run the request
            try:
                results = sem3.get_products()
                print(results)
                p = results['results'][0]['name']
            except:
                print('An error occured.')

            # View the results of the request
            print(p) 

            return Response({"upc":product_serializer.data,"result":p}, status=status.HTTP_201_CREATED)
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
