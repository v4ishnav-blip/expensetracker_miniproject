from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from expense.serializers import Userserializer,ExpenseSerializer
from expense.models import Expenses
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Sum,Count,Avg,Min,Max
from django.utils import timezone

# Create your views here.


class RegisterView(ViewSet):
    def create(self,request):
        dser=Userserializer(data=request.data)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

class ExpenseView(ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self,request):
        dser=ExpenseSerializer(data=request.data)
        if dser.is_valid():
            dser.save(owner=request.user)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        expenses=Expenses.objects.filter(owner=request.user)
        dser=ExpenseSerializer(expenses,many=True)
        return Response(data=dser.data,status=status.HTTP_200_OK)
    def destroy(self,request,pk=0):
        Expenses.objects.get(id=pk).delete()
        return Response(data={"msg":"Deleted"})
    def update(self,request,pk=0):
        expense_obj=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=request.data,instance=expense_obj)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)


class ExpenseSummaryView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        cur_date=timezone.now()
        cur_month=cur_date.month
        cur_year=cur_date.year
        print(cur_month,cur_year)
        data=Expenses.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        category_summary=data.values('category').annotate(Sum('amount'))
        ''''''
        [
            {'category':'fuel','total':3000},
            {'category':'bills','total':32000}
        ]
        ''''''
        cat_summary=[summery for summery in category_summary]
        print(cat_summary)
        for i in category_summary:
            print(i)
        total_expense=data.values('amount').aggregate(Sum('amount'))
        print(total_expense)
        # ser=ExpenseSerializer(qs,many=True)
        context={
            "total_expense":total_expense,
            "category_summary":dict[category_summary]
        }
        return Response(data=context)
