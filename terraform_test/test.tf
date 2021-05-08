terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token     = 
  cloud_id  = 
  folder_id = 
  zone      = 
}

data "template_file" "app_a_config" {
  template = file("app_a/cloud_config.yaml")

  vars = {
    db_hostname       = "${yandex_mdb_postgresql_cluster.postgres_db.host[0].fqdn}"
    db_user     = "default_user"
    db_password = "default_password"
    db_name = "app_database"
  }
}

data "template_file" "app_b_config" {
  template = file("app_b/cloud_config.yaml")

  vars = {
    db_hostname       = "${yandex_mdb_postgresql_cluster.postgres_db.host[0].fqdn}"
    db_user     = "default_user"
    db_password = "default_password"
    db_name = "app_database"
  }
}


resource "yandex_compute_instance" "vm-1" {
  name = "terraform1"

  resources {
    cores         = 2
    memory        = 1
    core_fraction = 5
  }

  boot_disk {
    initialize_params {
      image_id = "fd87va5cc00gaq2f5qfb"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

  metadata = {
    user-data = "${data.template_file.app_a_config.rendered}"
  }

  scheduling_policy {
    preemptible = true
  }

}

resource "yandex_compute_instance" "vm-2" {
  name = "terraform1"

  resources {
    cores         = 2
    memory        = 1
    core_fraction = 5
  }

  boot_disk {
    initialize_params {
      image_id = "fd87va5cc00gaq2f5qfb"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

  metadata = {
    user-data = "${data.template_file.app_b_config.rendered}"
  }

  scheduling_policy {
    preemptible = true
  }

}

resource "yandex_vpc_network" "network-1" {
  name = "network1"
}

resource "yandex_vpc_subnet" "subnet-1" {
  name           = "subnet1"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "yandex_lb_target_group" "app_a_group" {
  target {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    address   = yandex_compute_instance.vm-1.network_interface.0.ip_address
  }
}

resource "yandex_lb_target_group" "app_b_group" {
  target {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    address   = yandex_compute_instance.vm-2.network_interface.0.ip_address
  }
}


resource "yandex_lb_network_load_balancer" "balancer" {
  listener {
    name        = "appalistener"
    port        = 80
    target_port = 5000
    protocol    = "tcp"
    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.app_a_group.id

    healthcheck {
      name = "http"
      http_options {
        port = 5000
        path = "/ping"
      }
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.app_b_group.id

    healthcheck {
      name = "http"
      http_options {
        port = 5000
        path = "/ping"
      }
    }
   }
}

resource "yandex_mdb_postgresql_cluster" "postgres_db" {
  name        = "postgres_db"
  environment = "PRESTABLE"
  network_id  = yandex_vpc_network.network-1.id

  config {
    version = 12
    resources {
      resource_preset_id = "b1.nano"
      disk_type_id       = "network-hdd"
      disk_size          = 16
    }
  }

  database {
    name  = "app_database"
    owner = "default_user"
  }

  user {
    name     = "default_user"
    password = "default_password"
    permission {
      database_name = "app_database"
    }
  }

  host {
    zone      = "ru-central1-a"
    subnet_id = yandex_vpc_subnet.subnet-1.id
  }
}
