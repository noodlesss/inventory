import paramiko, time, openpyxl


cmd_eth0_mac = "ifconfig |  grep -B1 10.13.34 | grep HWaddr | awk {'print $5'}"
cmd_ipmi_mac = "ipmitool lan print | grep 'MAC Address' | awk {'print $4'}"
cmd_disk = "megacli -CfgDsply -aALL | grep 'Inquiry Data' | awk {'print $4'}"
cmd_cpu = "cat /proc/cpuinfo | grep 'model name' | awk '{$1=$2=$3=""; print}' | tail -1"
cmd_model = "dmidecode | grep -e 'Product Name:' | head -1 | awk {'print $3,$4'}"
cmd_serial = "dmidecode | grep -e 'Serial Number:' | head -1 | awk {'print $3'}"
cmd_list=[cmd_eth0_mac, cmd_ipmi_mac, cmd_disk, cmd_cpu, cmd_model, cmd_serial]



with open('inventory.log') as fl:
	inventory = fl.read()

inventory_list = inventory.split('\n')
d = {}


def ssh(hostname, d, inventory_info=[]):
	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname, username='<username>', key_filename='<path/to/openssh-private-key-file>')
	for cmd in cmd_list:
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
		time.sleep(1)
		inventory_info.append(ssh_stdout.read(9999))
	d[hostname] = inventory_info
	

if __name__=='__main__':
	for hostname in inventory_list:
		ssh(hostname, d)
	print d
	wb = openpyxl.load_workbook('inv.xlsx')
	sheet = wb.get_sheet_by_name('Sheet1')
	#d = {'asd':[111,222,333,444,555,666], 'bbb':[111,222,333,444,555,666],'ccc':[111,222,333,444,555,666]}
	for i in range(row):
		print i
		sheet['A'+str(i+2)] = d.keys()[i]
		for n in range(len((d.values()[0]))):
			sheet.cell(row=i+2, column=n+2).value = d.values()[0][n]

	wb.save('asd.xlsx')