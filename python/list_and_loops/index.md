# List_and_loops


# Lists and Loop

```python
empty_list = []
print(empty_list)
str_list = ["hello","world","4.5"]
print(str_list)
print("The first item of str_list is " + str(str_list[0])) # Refer to a item in the list

mixed_list=["hello",100,4.5]
print(mixed_list)
mixed_list.append("AppendedItem") # Append method
print(mixed_list)
if "AppendedItem" in mixed_list:
    mixed_list.remove("AppendedItem") # Remove method
    print("AppendedItem is exist and removed")
print(mixed_list)

del mixed_list[0] # Use del if you want to use the sequence number
print(mixed_list)

list_list = [empty_list,str_list,mixed_list]
print(list_list)

for x in list_list:
    print(x)
```

# Range

```python
expenses = []
total = 0

num_expenses = int(input("Enter nubmer of expenses:\n"))

for i in range(num_expenses):
    expenses.append(float(input("How much is expense #" + str(i) + ":")))

total = sum(expenses)

print("You have spent totally $" + str(total))
```

# Loan caculator

```python
# What is the annual percentage rate?\n
apr = float(input("What is the annual percentage rate?\n")) #6
# How much do you owe， in dollars?\n
money_owned = float(input("How much do you owe， in dollars?\n")) #100000
# How much you want to pay each month?\n
payment = float(input("How much you want to pay each month?\n")) #2000
# How many months do you want to see results for?\n
months = int(input("How many months do you want to see results for?\n")) #58

# convert apr to monthly rate
monthly_rate = apr/100/12

for i in range(months):
    # Add in interest
    interest_paid = money_owned*monthly_rate
    money_owned = money_owned+interest_paid

    # Make a payment
    if money_owned < payment:
        # Result after the last payment
        print("You have paid off in ",i+1," monthes and the last payment is $",money_owned,sep="")
        money_owned = 0
        break
    else:
        money_owned = money_owned-payment
        # Result after payment
        print("Interest paid $",interest_paid,"Now you owe $",money_owned,sep="")

```
