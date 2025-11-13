from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsProOrAdmin
class ProStatsView(APIView):
    permission_classes = [IsAuthenticated, IsProOrAdmin]

    def get(self, request):

        return Response({
            "total_sales": 0,
            "nfts_listed": 0,
            "favourite_chain": "Ethereum",
            "active_listings": 0,
            "monthly_revenue": 0,
            "top_selling_nft": None,
            "recent_sales": [],
        })