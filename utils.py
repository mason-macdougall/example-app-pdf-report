import numpy as np

def get_gas_cost(job, car):
    
    if str(job['dist']) != 'nan':# in job.keys():
        job_dist = job['dist']
    elif str(job['travel_time']) != 'nan' and str(car['mph']) != 'nan':
        job_dist = (job['travel_time']/60.) * car['mph']
    else:
        'Error: Must have either \'dist\' in job dict\nor \'travel_time\' in job dict and \'mph\' in car dict'
        return np.nan
    
    if str(car['mpg']) != 'nan':
        mpg = car['mpg']
    elif len(car['miles_tanksize_fraction']) != 3:
        miles, tank, frac = car['miles_tanksize_fraction']
        gals = tank*frac
        mpg = miles/gals
    else:
        'Error: Must have either \'mpg\' or \'miles_tanksize_fraction\' in car dict'
        return np.nan
    
    tot_dist_traveled = (2*job_dist) * job['days']
    tot_gas_gals = tot_dist_traveled / mpg
    gas_cost = tot_gas_gals * car['gas']
    return gas_cost



def get_pay(job):
    pay_per_week = job['hours'] * job['pay']
    if str(job['overtime_hours']) != 'nan' and str(job['overtime_pay']) != 'nan':
        pay_per_week += job['overtime_hours'] * job['overtime_pay']
    return pay_per_week


    
def get_travel_time(job, car):
    if str(job['dist']) != 'nan' and str(car['mph']) != 'nan':
        travel_time = (job['dist'] / car['mph']) * 60.
    elif str(job['travel_time']) != 'nan':
        travel_time = job['travel_time']
    else:
        'Error: Must have either \'travel_time\' in job dict\nor \'dist\' in job dict and \'mph\' in car dict'
        return np.nan
    
    travel_tot = (2*travel_time) * job['days']
    return travel_tot / 60. # in hours
        
    

def get_net_earnings(job, car, tax_rate=None):
    
    if tax_rate == None:
        tax_rate = 0
    
    # Gas costs
    gas_cost = get_gas_cost(job, car)
    
    # Weekly pay
    earnings = get_pay(job) * (1-tax_rate)
    
    job_result = {'net': earnings - gas_cost, 'pay': earnings, 'gas': gas_cost}
    
    return job_result



def get_effective_pay(job, car, tax_rate=None):
    if tax_rate == None:
        tax_rate = 0.0

    job_earnings = get_net_earnings(job, car, tax_rate=tax_rate)
    job_travel = get_travel_time(job, car)
    
    if str(job['overtime_hours']) == 'nan':
        overtime = 0
    else:
        overtime = job['overtime_hours']
        
    hours_tot = job['hours'] + overtime + job_travel
    
    if hours_tot > 0:
        eff_pay = job_earnings['net'] / hours_tot
    else:
        eff_pay = 0

    return eff_pay
    


def get_full_report(job1, job2, car, tax_rate=None):

    jobs = [job1, job2]

    reports = {}

    for i, job in enumerate(jobs):
        job_earnings = get_net_earnings(job, car, tax_rate=tax_rate)
        job_travel = get_travel_time(job, car)

        report = {'travel_time': job_travel}
        report.update(job_earnings)

        reports[i] = report

    val = 'net'
    val1, val2 = reports[0][val], reports[1][val]
    ii = np.argmax([val1, val2])
    jj = np.argmin([val1, val2])

    net_best = round(reports[ii]['net'], 2)
    net_diff = round(reports[ii]['net'] - reports[jj]['net'], 2)
    net_pay = round(reports[ii]['pay'] - reports[jj]['pay'], 2)
    net_gas = round(reports[ii]['gas'] - reports[jj]['gas'], 2)
    diff_travel = round(reports[ii]['travel_time'] - reports[jj]['travel_time'], 2)

    lost_pay = round(diff_travel * jobs[jj]['pay'], 2)

    print_list = []

    print_list.append(f'Job #{ii+1} provides more net income! Totaling ${net_best} per week (accounting for gas spendings)')
    print_list.append(f'- You will take home ${net_diff} MORE each week than at Job #{jj+1} (accounting for gas spendings)')
    print_list.append('')
    print_list.append('')
          
    #      Your total weekly income at Job #{ii+1} will be ${net_diff} MORE than at Job #{jj+1}\n')
    print_list.append(f'But here\'s other information worth knowing about Job #{ii+1}:')
    
    npay = np.abs(net_pay)
    ngas = np.abs(net_gas)
    
    if net_pay >= 0 and net_gas <= 0:
        print_list.append(f'- Your paycheck will be ${npay} MORE than it would be for Job #{jj+1}')
        if net_gas < 0:
            print_list.append(f'- AND you will spend ${ngas} LESS on gas compared to Job #{jj+1}')
    elif net_pay >= 0 and net_gas >= 0:
        print_list.append(f'- Your paycheck will be ${npay} MORE than it would be for Job #{jj+1}')
        if net_gas > 0:
            print_list.append(f'- BUT you will spend ${ngas} MORE on gas compared to Job #{jj+1}')
    elif net_pay <= 0 and net_gas <= 0:
        print_list.append(f'- Your paycheck will be ${npay} LESS than it would be for Job #{jj+1}')
        if net_gas < 0:
            print_list.append(f'- BUT you will spend ${ngas} LESS on gas compared to Job #{jj+1}')
        
        
        
        
    eff_pay_ii = round(get_effective_pay(jobs[ii], car, tax_rate=tax_rate), 2)
    eff_pay_jj = round(get_effective_pay(jobs[jj], car, tax_rate=tax_rate), 2)
    
    if diff_travel != 0:
        if diff_travel > 0:
            stime = 'MORE'
        elif diff_travel < 0:
            stime = 'FEWER'
        else:
            return ['Error: Travel time calculation failed! Re-check inputs']
        print_list.append(f'- You will also waste {np.abs(diff_travel)} {stime} hours commuting compared to Job #{jj+1}')


        print_list.append('')
        print_list.append('')

        print_list.append('Accounting for gas spendings, travel time, any overtime, and taxes (if applicable):')
        print_list.append(f'- Effective hourly pay rate for Job #{ii+1}: ${eff_pay_ii} per hour') #'- You will also waste {np.abs(diff_travel)} {stime} hours commuting compared to Job #{jj+1}')
        print_list.append(f'- Effective hourly pay rate for Job #{jj+1}: ${eff_pay_jj} per hour') #

        if eff_pay_ii > eff_pay_jj:
            print_list.append('')
            print_list.append('')
            print_list.append(f'FINAL ASSESSMENT: Job #{ii+1} earns you MORE net income AND pays you MORE for your time spent working + commuting')
            if eff_pay_ii >= 7.25:
                print_list.append(f'                  Definitely go with Job #{ii+1}!')
            else:
                print_list.append(f'                  WARNING: Your effective pay will be lower than the US national minimum wage of $7.25')
                print_list.append(f'                  Choose wisely!')

        elif eff_pay_ii < eff_pay_jj:
            print_list.append('')
            print_list.append('')
            print_list.append(f'FINAL ASSESSMENT: Job #{ii+1} earns you MORE net income BUT pays you LESS for your time spent working + commuting')
            print_list.append(f'                  If you value your time more, choose Job #{jj+1}')
            print_list.append(f'                  If you value earning money more, choose Job #{ii+1}')
            if eff_pay_ii < 7.25:
                print_list.append(f'                  WARNING: Your effective pay for Job #{ii+1} would be lower than US national minimum wage of $7.25')
            if eff_pay_jj < 7.25:
                print_list.append(f'                  WARNING: Your effective pay for Job #{jj+1} would be lower than US national minimum wage of $7.25')
            print_list.append(f'                  Choose wisely!')

    else:
        print_list.append('')
        print_list.append('')
        print_list.append(f'FINAL ASSESSMENT: Job #{ii+1} earns you MORE net income and your travel time is roughly the same for either job')
        print_list.append(f'                  Definitely go with Job #{ii+1}!')
    
    '''    
    if diff_travel != 0:
        if diff_travel > 0:
            stime = 'MORE'
        elif diff_travel < 0:
            stime = 'FEWER'
        else:
            return ['Error: Travel time calculation failed! Re-check inputs']
        print_list.append(f'- You will also waste {np.abs(diff_travel)} {stime} hours commuting compared to Job #{jj+1}')

        if diff_travel > 0:
            new_net_diff = round(net_diff-lost_pay, 2)
            print_list.append('')
            print_list.append(f'- If each hour of travel time is worth the hourly pay rate from Job #{jj+1},')
            print_list.append(f'  then you LOSE an additional ${lost_pay} in time wasted traveling to Job #{ii+1}') #Extra travel time for Job #{ii+1} is equivalent to ${lost_pay} of potential pay \n  that you miss out on (assuming pay rate from Job #{jj+1})')

            if new_net_diff > 0:
                print_list.append(f'- Hypothetically, this brings the difference in net income down to ${new_net_diff},')
                print_list.append(f'                  so Job #{ii+1} would still be BETTER than Job #{jj+1}')
                print_list.append('')
                print_list.append('')
                print_list.append(f'FINAL ASSESSMENT: Even with travel time, Job #{ii+1} is better in terms of income and travel time!')

            elif new_net_diff < 0:
                print_list.append(f'- Hypothetically, this means that you are LOSING ${np.abs(new_net_diff)} in total TIME + MONEY at Job #{ii+1}')  #is actually MORE worth your time than Job #{ii+1}\n                  i.e. Your net income for Job #{jj+1} is now ${np.abs(new_net_diff)} HIGHER than for Job #{ii+1}')
                print_list.append('')
                print_list.append('')
                print_list.append(f'FINAL ASSESSMENT: Job #{ii+1} puts more money in your bank, but ')
                print_list.append(f'                  Job #{jj+1} is better when accounting for time wasted traveling to Job #{ii+1}.')
                print_list.append(f'                  Choose wisely!')

        elif diff_travel < 0:
            print_list.append('')
            print_list.append('')
            print_list.append(f'FINAL ASSESSMENT: Job #{ii+1} is definitely the better option in terms of income and travel time!')
    else:
        print_list.append('')
        print_list.append('')
        print_list.append(f'FINAL ASSESSMENT: Job #{ii+1} is definitely the better option in terms of income and travel time!')
    '''
    
    
    print_list.append('')
    print_list.append('')

    if tax_rate == None:
        print_list.append('NOTE: This analysis does not consider income taxes')
    else:
        tr = round(tax_rate*100,2)
        print_list.append(f'NOTE: This analysis assumes an income tax rate of {tr}%')
        
    if (str(job1['overtime_hours']) not in ['nan', '0', '0.0'] and str(job1['overtime_pay']) not in ['nan', '0', '0.0']) or (str(job2['overtime_hours']) not in ['nan', '0', '0.0'] and str(job2['overtime_pay']) not in ['nan', '0', '0.0']):
        print_list.append(f'NOTE: This analysis includes overtime pay')

    if diff_travel != 0:
        print_list.append(f'NOTE: Effective hourly pay rate is calculated by (total pay - total spent on gas) / (hours worked + hours commuting)')

        
    return print_list

    

    
