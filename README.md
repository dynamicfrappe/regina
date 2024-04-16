## Regina

Regina Resort

#### License

MIT


### main Domain Time 
Time Share

Main Company 
      User should save company Address in Company Doctype  
### Master Data 
Customer - Agent - Contract - Contract Serial - Contract Type - Unit -Reservation 
##  Contract Management 
Contract 
Contract Type -- name add contract template as text 
Contract Serial Number  -- unique number with type and room Type / 




Send Contract To Agent 
Receive Contract  from Agent 
calculate Agent  contracts 

##  Office Management System 
data 
representative -- object linked with email/user -- done
 have static values name /Phone Number /Office Number (if user set) 
-- has status
-- representative should have system user email 
When user login system set representative on line 
When user log out system set representative off line 

Channels / visit / whatsApp / Phone 

Action / channel link to channel Type 
Agent type / Customer / Lead / Opportunity 
Agent  link to current Object 
Notes 
Assign to representative  / get Current Available Representative






##  Contract Management  / done
##  Office Management System /done
##  Collections Management
##  Archive System
## Unit Reservation

###  Customize 
 Customer DocType
 Item DocType 

-- room number 
-- room type (one , two or three beds)  --link new doctype ( initial values) 
-- room view (see th see or not)  - link 
-- brand -- we will make resort as brand 
-- location -- select -- doctype -- resort ()

contract 
Add Brand  , Item Group and Room Type To contract info  
Payment terms        -- added to contract 
Annual Services Type -- added to contract to add any service will payed annual 
Create Week Ben List To get Available Weeks For item and reserved weeks 
Create Week Ben Ledger To get Unit Validation For Buying 



## Archived System 

Document typ -- payment or item 
Date 
customer 
Amount




in Management Settings Add Filed Default Tax Template -- link selling tax template 
# in agent Agent Price List  -- set 
Agent fees Tax read only 
Agent fee discount Tax read only  
calculate the tow fees depend on Agent fees 
Advance payment + Total Reserved Payments = Total Payment Amount validation /auto calculate 
 on agent save set annual services data 

 ## Annual Services Template

  create template with required data for services fees







## Unit Reservation  

create year doctype should be valid year from range (1990 - to 2050) 
how it work 

reception send customer to sales man 

in customer reservation page  we need to  ad view button under view add two button show history /reservation history 
show history is a report to get all customer archived data / payments / 
reservation history show all reservation logs 
fields 

customer   -- link to customer 
year       -- link to year
from date  -- date field 
to date    -- date field  
contract   -- link to contract 
brand      -- link to brand --from contract
item group -- link to item group --from contract
Room Type  --  link to Room Type -- from contract 
unit       -- link to item 

unit filter -- get all item with no reservation in date range with apply filetrs brand / item group /room type 


#customer reservation ledger 
where contract created system should create customer ledger 
depend on contract weeks count / week days count will set by user in Management Settings filed name week days 


#reservation_bin doctype 
fields unit --link to item /
customer link to customer /
contract link to contract 
date from - date to /
days count - number / read only /calculate days count from start to end 
agent /
year --link to year doctype 
unit location /
unit view 

# unit reservation bin unit year --link to year 
each year has its bin  / each item has one bin for one year / 
available unit is the second field  it should be 366 day 
reserved days float field (should be the sum of all reserved days in unit with same year)

valid days ==> count(availd-reserved)

 

