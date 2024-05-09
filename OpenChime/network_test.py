def get_net_interfaces():
	interface_paths = {"eth0", "wlan0"}
	interface_path = "/sys/class/net/"
	interfaces = []
	for interface in interface_paths:
		f = open(interface_path+interface+"/operstate")
		text = f.read()
		f.close()
		if "up" in text:
			interfaces.append(interface)
	return interfaces