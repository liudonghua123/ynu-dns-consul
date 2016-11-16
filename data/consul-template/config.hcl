token= "a5c882f6-02b5-95ea-8698-8189b55abacc"
template {
  source = "/data/consul-template/dns.ct"
  destination = "/etc/named/db.ynu.edu.cn"
  command= "named-checkconf && named-checkzone ynu.edu.cn /etc/named/db.ynu.edu.cn && rndc reload"
}
