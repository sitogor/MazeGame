
# Grids = [0,1,2,8,7,13,14,15,21,22,17,16]
# Grids = [0,1,7,8,9,10,11,14,15,17,23,29,35]
Grids = [0,1,2,3,8,9,12,13,14,18,19,20,24,30,31,32,33,34,35]
start = 0
end = 35
size = 6
tot = {}
def path_det(Grid_num, start,end):
#    print(Grid_num)
    direction =[]
    if (Grid_num+1) in Grids:
        direction.append(Grid_num+1)
        # Grids_1.remove(Grid_num)
    if (Grid_num+size) in Grids:
        direction.append(Grid_num+size)
        # Grids_1.remove(Grid_num)
    if (Grid_num - 1) in Grids:
        direction.append(Grid_num-1)
        # Grids_1.remove(Grid_num)
    if (Grid_num - size) in Grids:
        direction.append(Grid_num-size)
    if len(direction)==0 or Grid_num==end:
        direction = [start]
    #Grids_1.remove(Grid_num)

    return direction


# making a list of the removable items in the list
def remove_func():
    remove_list =[]
    for y in Grids:
        if len(tot[y])==1:
    #            print(y,tot[y], len(tot[y]))
                remove_list.append(tot[y][0])
    return remove_list


#removing possible directions to blocks if another block can only move to that block 
def route_recog(new_tot,remove_ls):
    for u in Grids:
        if len(new_tot[u])>1:
    #        print(tot[u])
            for x in remove_ls:
                if x in new_tot[u]:
                    new_tot[u].remove(x)
    return(new_tot)


# removing all the not possible routes where the ball could be stuck between 2 grids, input of the newest tot dictionary
def not_poss(new_tot):
    # key_list = list(new_tot.keys())
    # print(key_list)
    for y in Grids:
        if len(new_tot[y])==1:
            g = new_tot[y][0]
            if y in new_tot[g]:
                new_tot[g].remove(y)
    return(new_tot)


# getting the final dictionary and working out the direction the ball has to take once in a certain grid
def directions(tot_final,size):
    final_route={}
    # turning single value lists into just the integers
    for x in Grids:
        tot_final.update({x:tot_final[x][0]})
    #getting directions for each grid number
    for x in Grids:
        if x==tot_final[x]+1:
            direction = 'l'
        elif x==tot_final[x]-1:
            direction = 'r'
        elif x==tot_final[x]+size:
            direction = 'u'
        elif x==tot_final[x]-size:
            direction = 'd'
        else:
            direction = 'end'
        final_route[x]=direction
    return final_route


# rem = remove_func()
# print(rem)
for x in range(len(Grids)):
    maze = path_det(Grids[x],start,end)
    tot[Grids[x]] = maze
# print (tot)
finished =False


while finished ==False:
    list_len=0
    for x in Grids:
        list_len+=len(tot[x])
    if list_len==len(tot):
        print(directions(tot,6))
        finished = True
    else:
        rem=remove_func()
        tot=route_recog(tot,rem)
        tot=not_poss(tot)
        # print(tot)
        finished = False

# tot1=route_recog(tot,rem)
# print(tot1)
# rem1=remove_func()
# print(rem1)
# for x in range(10):
#     tot1=route_recog(tot1,rem1)
#     rem1=remove_func()

# print(tot1)
# print(rem1)
# tot1 = not_poss(tot1)
# print(tot1)
# for x in range(10):
#     tot1=route_recog(tot1,rem1)
#     rem1=remove_func()
# print(tot1)

# print(directions(tot1,6))
