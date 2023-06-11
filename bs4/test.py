import pandas as pd

states = ["California","Texas","Florida","New York"]
population = [39613493,29730311,21944577,19299981]

dictionary_states = {'States':states,'Population':population}

# create data frame
df_states = pd.DataFrame.from_dict(dictionary_states)
print(df_states)

# export to csv file
df_states.to_csv('states.csv',index=False)

# for state in states:
# if state == 'Florida':
#     print(state)


# with open('test.txt','w') as file:
#     file.write("Data successfully scraped!")


