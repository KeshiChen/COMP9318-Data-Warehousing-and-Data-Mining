select location, time, item, sum(quantity) 
from test 
group by location, time, item
union
select location, time, '0', sum(quantity)
from test
group by location, time
union
select location, 0, item, sum(quantity)
from test
group by location, item
union
select location,0,'0', sum(quantity)
from test
group by location
union
select '0', time, item, sum(quantity) 
from test 
group by  time, item
union
select '0', time, '0', sum(quantity) 
from test 
group by  time
union
select '0', 0, item, sum(quantity) 
from test 
group by  item