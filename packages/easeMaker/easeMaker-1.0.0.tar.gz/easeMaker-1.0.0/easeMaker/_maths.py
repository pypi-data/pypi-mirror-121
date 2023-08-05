class Maths:
    def increment(self,var,by):
        var = var + by
    def decrement(self,var,by):
        var = var - by
    
    def get_perimeter_of_rect(self,length,width):
        return (length+width)*2
    def get_area_of_rect(self,length,width):
        return length*width
    def get_perimeter_of_square(self,side):
        return 4*side
    def get_area_of_square(self,side):
        return side*side
    def get_volume_of_cuboid(self,length,width,height):
        return length*width*height
    def get_profit(self,selling_price,cost_price):
        if(selling_price > cost_price):
            amount = selling_price - cost_price
            return amount
        elif selling_price == cost_price:return 0
        else:return None
    def get_loss(self,cost_price,selling_price):
        if(cost_price > selling_price):
            amount = cost_price - selling_price
            return amount
        elif cost_price == selling_price:return 0
        else:return None  