import unittest 
import cli
from runner import subp

class Test_pv_create(unittest.TestCase):
    
    def setUp(self):
        print("step 1 : creating PV")
        subp(f"sudo pvcreate {cli.disk}")

    def tearDown(self):
        print("step 3 : removing pv")
        subp("sudo pvremove {cli.disk}")

    def testpv(self):
        print("step 2 : ")
        for i in cli.d:
            print(f"Test to chech {i} physical volume is created")
            self.assertRegex(subp("sudo pvdisplay").stdout, i)


class Test_vg_create(unittest.TestCase):

    def setUp(self):
        print("step 1 : creating pv and vg")
        subp(f"sudo pvcreate {cli.disk}")
        subp(f"sudo vgcreate {cli.vg_name} {cli.disk}")

    def tearDown(self):
        print("step 3 : deleting pv and vg")
        subp(f"sudo vgremove {cli.vg_name}")
        subp(f"sudo pvremove {cli.disk}")

    def testvg(self):
        print(f"Step 2 : Test to check {cli.vg_name} volume group is created")
        self.assertRegex(subp("sudo vgdisplay").stdout, cli.vg_name) 

class Test_lv_create(unittest.TestCase):

    def setUp(self):
        print("step 1 : creating pv and vg")
        subp(f"sudo pvcreate {cli.disk}")
        subp(f"sudo vgcreate {cli.vg_name} {cli.disk}")
        subp(f"sudo lvcreate -n {cli.lv_name} --size {cli.lv_size}G {cli.vg_name}")
       
    def tearDown(self):
        print("step 3 : deleting pv vg lv")
        subp(f"sudo lvremove -ff {cli.vg_name}")
        subp(f"sudo vgremove {cli.vg_name}")
        subp(f"sudo pvremove {cli.disk}")


    def testlv(self):
        print(f"Step 2 : Test to check {cli.lv_name} logical volume is created")
        self.assertRegex(subp(f"sudo lvdisplay").stdout, cli.lv_name)


class Test_fs_fio(unittest.TestCase):

    def setUp(self):
        print("step 1: creating pv vg lv")
        
        subp(f"sudo pvcreate {cli.disk}")
        subp(f"sudo vgcreate {cli.vg_name} {cli.disk}")
        subp(f"sudo lvcreate -n {cli.lv_name} --size {cli.lv_size}G {cli.vg_name}")
        
        self.mountpoint = "/data"
        self.lvpath = f"/dev/{cli.vg_name}/{cli.lv_name}"
        
        print("step 2 : creating file system")
        subp(f"sudo mkfs.{cli.fs} {self.lvpath}")
        subp("mkdir {self.mountpoint}")
        subp(f"mount {self.lvpath} {self.mountpoint}")
       

    def tearDown(self):
        print("\n\nstep 8 : destroying the physical volume, volume group, logical volume")
        subp(f"sudo umount /data")
        subp(f"sudo lvremove -ff {cli.vg_name}")
        subp(f"sudo vgremove {cli.vg_name}")
        subp(f"sudo pvremove {cli.disk}")
        
    def testfs(self):
        
        print("\nstep 3 : to check pv is created")
        for i in cli.d:
            print(i)
            self.assertRegex(subp("sudo pvdisplay").stdout, i)
            print("sucess")

        print("\nstep 4 : to check vg is created")
        self.assertRegex(subp("sudo vgdisplay").stdout, cli.vg_name)
        print("sucess")

        print("\nstep 5 : to check lv is created")
        self.assertRegex(subp("sudo lvdisplay").stdout, cli.lv_name)
        print("sucess")

        print("\nstep 6 : to check file system is mounted")
        self.assertRegex(subp("df -h").stdout, self.mountpoint)
        print("sucess")

        print("\nstep 7:performing and verifying IO")
        self.assertRegex(subp("fio fiorandread.fio").stdout, "Run status")
        print("sucess")

