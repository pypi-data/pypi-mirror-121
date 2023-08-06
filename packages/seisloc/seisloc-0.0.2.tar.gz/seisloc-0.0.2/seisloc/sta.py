import re
from obspy.geodetics import gps2dist_azimuth

def sta_dist_pairs(netstas,sta_dict,group_qty=6):
    pair_list = []
    for netsta1 in netstas:     # loop for each sta
        net1 = netsta1[:2]
        sta1 = netsta1[2:]
        lon1 = sta_dict[net1][sta1][0]
        lat1 = sta_dict[net1][sta1][1]
        dist_list = []
        for netsta2 in netstas: # calculate distance one by one
            net2 = netsta2[:2]
            sta2 = netsta2[2:]
            lon2 = sta_dict[net2][sta2][0]
            lat2 = sta_dict[net2][sta2][1]  
            dist,_,_ = gps2dist_azimuth(lat1,lon1,lat2,lon2)
            dist_list.append(dist)
        dist_list_cp = dist_list.copy()
        dist_list_cp.sort()
        for i in range(1,min([group_qty+1,len(netstas)])): # 0 idx is self
            dist = dist_list_cp[i]
            idx = dist_list.index(dist)
            tmp_netsta = netstas[idx]
            if [netsta1,tmp_netsta] not in pair_list and\
               [tmp_netsta,netsta1] not in pair_list:
                pair_list.append([netsta1,tmp_netsta])      
    return pair_list

def load_sta(sta_file):
    sta_dict={}
    with open(sta_file,'r') as f:
        for line in f:
            line = line.rstrip()
            net,sta,_lon,_lat,_ele,label=re.split(" +",line)
            if net not in sta_dict:
                sta_dict[net]={}
            if sta not in sta_dict[net]:
                sta_dict[net][sta] = [float(_lon),float(_lat),int(_ele),label]
    return sta_dict

def to_inv_sta_file(sta_dict,out_file,ele_zero=True):
    f_inv = open(out_file,'w')
    for net in sta_dict.keys():
        for sta in sta_dict[net].keys():
            lon = sta_dict[net][sta][0]
            lat = sta_dict[net][sta][1]
            ele = sta_dict[net][sta][2]
            label = sta_dict[net][sta][3]
            net_sta = net+sta
            lon_i = int(lon)
            lon_f = lon-lon_i
            lat_i = int(lat)
            lat_f = lat-lat_i
            if ele_zero:
                ele = 0
            f_inv.write(format(sta,"<6s")+format(net,"<4s")+"SHZ  "+format(lat_i,">2d")+" "+\
                format(lat_f*60,">7.4f")+" "+format(lon_i,">3d")+" "+format(lon_f*60,">7.4f")+\
                "E"+format(ele,">4d")+"\n")
    f_inv.close()

def sta2inv(sta_file,out_file):
    """
    Convert station file into hypoinverse format
    """
    sta_dict =load_sta(sta_file)
    to_inv_sta_file(sta_dict,out_file)  # Write into files

def to_dd_sta_file(sta_dict,out_file,ele_zero=True):
    f_dd = open(out_file,'w')
    for net in sta_dict.keys():
        for sta in sta_dict[net].keys():
            lon = sta_dict[net][sta][0]
            lat = sta_dict[net][sta][1]
            ele = sta_dict[net][sta][2]
            label = sta_dict[net][sta][3]
            net_sta = net+sta
            lon_i = int(lon)
            lon_f = lon-lon_i
            lat_i = int(lat)
            lat_f = lat-lat_i
            if ele_zero:
                ele = 0
            f_dd.write(format(net_sta,"<9s")+format(lat_i+lat_f,">9.6f")+format(lon_i+lon_f,">12.6f")+\
                   " "+format(ele,'>5d')+"\n")
    f_dd.close()

def sta2dd(sta_file,out_file):
    """
    Convert station file into hypoDD format
    """
    sta_dict = load_sta(sta_file)
    to_dd_sta_file(sta_dict,out_file)  # Write into files

def to_vel_sta_file(sta_dict,out_file,ele_zero=True):
    f_vel = open(out_file,'w')
    f_vel.write("(a5,f7.4,a1,1x,f8.4,a1,1x,i4,1x,i1,1x,i3,1x,f5.2,2x,f5.2,3x,i1)\n")
    sta_count = 1
    for net in sta_dict.keys():
        for sta in sta_dict[net].keys():
            lon = sta_dict[net][sta][0]
            lat = sta_dict[net][sta][1]
            ele = sta_dict[net][sta][2]
            label = sta_dict[net][sta][3]
            if ele_zero:
                ele = 0
            f_vel.write(f"{format(sta,'<5s')}{format(lat,'7.4f')}N {format(lon,'8.4f')}E {format(ele,'4d')} 1 "+\
                f"{format(sta_count,'3d')} {format(0,'5.2f')}  {format(0,'5.2f')}   1\n")
            sta_count += 1
    f_vel.write("  \n")   # signal of end of file for VELEST
    f_vel.close()

def sta2vel(sta_file,out_file,ele_zero=True):
    """
    Convert station file into VELEST format with 5 characters,
    which is applicable for the update VELEST program modified by Hardy ZI
    """
    sta_dict = load_sta(sta_file)
    to_vel_sta_file(sta_dict,out_file,ele_zero)
