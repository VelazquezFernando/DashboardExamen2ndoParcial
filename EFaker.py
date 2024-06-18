from faker import Faker
import pandas as pd


fake = Faker(locale='es')

# print(fake.name())
#print(fake.address())


def create_employees(num_employees):
    employee_list = []
    
    for i in range(1, num_employees):
        employee = {}
        employee['fecha inicio'] = fake.century()
        employee['first_name'] = fake.first_name()
        employee['last_name'] = fake.last_name()
        employee['job'] = fake.job()
        employee['departamento'] = fake.random_element(elements=("IT","HR", "Marketing", "Finance"))
        employee['role'] = fake.random_element(elements=("Manager","Developer", "Analyst", "Asociate"))
        employee['salary'] = fake.random_int(min=3000, max=150000, step=1000)
        employee['email'] = fake.email()
        employee_list.append(employee)
    return pd.DataFrame(employee_list)





#print(create_employees(6))
print("generando")
#data = create_employees(10)

#data.to_csv('employee.csv')
start_date = "1999-02-02"
end_date = "1999-03-03"

Faker.seed(0)
for i in range(1, 10):
    print(fake.date())


print("FIN generacion")