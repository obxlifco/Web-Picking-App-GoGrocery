import { DatePipe } from '@angular/common';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { CommonfunctionService } from 'src/app/core/utilities/commonfunction.service';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';

@Component({
  selector: 'app-editstore',
  templateUrl: './editstore.component.html',
  styleUrls: ['./editstore.component.scss']
})
export class EditstoreComponent implements OnInit {
  @ViewChild('phoneNumber1', { static: false }) phonenumber: ElementRef | any;
  contactperson: any
  phoneNumber: any=''
  deliverTimeModifier: any
  paymentmethod: any = []
  allComplete: boolean = false;
  paymentmethodid: any
  paymentmethodname: any
  warehouse_id: any
  website_id: any;
  userID: any;
  storeData: any = []
  isSaved = true
  constructor(public apiService: ApiService, public commonfunc: CommonfunctionService,
    public globalitem: GlobalitemService, public datePipe: DatePipe,
    public db: DatabaseService) {
    this.paymentmethod = commonfunc.getPaymentMethod()
    this.getwarehouseData()
  }
  ngOnInit(): void {
    this.storeData["data"] = []
  }
  //checkbox
  updateAllComplete() {
    this.allComplete = this.paymentmethod.subtasks != null && this.paymentmethod.subtasks.every((t: { completed: any; }) => t.completed);
  }

  someComplete(): boolean {
    // console.log("some completed : ");
    if (this.paymentmethod.subtasks == null) {
      return false;
    }
    return this.paymentmethod.subtasks.filter((t: { completed: any; }) => t.completed).length > 0;
  }

  setAll(completed: boolean) {
    if (this.paymentmethod.subtasks == null) {
      return;
    }
    this.paymentmethod.subtasks.forEach((t: { completed: boolean; }) => t.completed = completed);
  }
  getwarehouseData() {
    for (let j = 0; j < this.paymentmethod.subtasks.length; j++) {
      this.paymentmethod.subtasks[j].completed = false
    }
    this.db.getUserData().then(res => {
      this.userID = res.user_id
      this.warehouse_id = res.warehouse_id
      this.website_id = res.website_id
      this.apiService.getData("warehouse/" + res.warehouse_id + "/").subscribe((data: any) => {
        this.storeData["data"] = data
        this.contactperson = this.storeData["data"].warehouse.contact_person;
        this.phoneNumber = this.storeData["data"].warehouse.phone;
        this.deliverTimeModifier = this.storeData["data"].warehouse.expected_delivery_time

        for (let i = 0; i < this.storeData["data"].payment_option.length; i++) {
          for (let j = 0; j < this.paymentmethod.subtasks.length; j++) {
            if (this.storeData["data"].payment_option[i].payment_method_id === this.paymentmethod.subtasks[j].id) {
              // console.log("payment id : ", this.paymentmethod.subtasks[j]);

              this.paymentmethod.subtasks[j].completed = true
            }
          }
        }
      })
    })
  }
  savestoreInfo() {
    this.db.getUserData().then(res => {
      // console.log("payment method ID : ", this.rangeFormGroup.controls.paymentmethodid.value);
      let store_category_type: any = []
      let managerids: any = ""
      let paymentids: any = []
      let warehouse_category: any = []
      // console.log("number length : ",this.phonenumber.nativeElement.value.length);
      
      if (this.phonenumber.nativeElement.value.length >= 10 && this.phonenumber.nativeElement.value.length <= 12) {
        this.isSaved = false
        for (let i = 0; i < this.storeData["data"].store_type.length; i++) {
          store_category_type.push(this.storeData["data"].store_type[i]?.type)
        }
        for (let i = 0; i < this.storeData["data"].users.length; i++) {
          if (this.storeData["data"].users[i].status)
            managerids += this.storeData["data"].users[i]?.id + ","
        }
        for (let i = 0; i < this.paymentmethod.subtasks.length; i++) {
          if (this.paymentmethod.subtasks[i].completed)
            paymentids.push(this.paymentmethod.subtasks[i]?.id)
        }
        for (let i = 0; i < this.storeData["data"].warehouse_category.length; i++) {
          warehouse_category.push(this.storeData["data"].warehouse_category[i]?.category)
        }
        if (this.storeData["data"].warehouse.channel_id === null) {
          this.storeData["data"].warehouse.channel_id = ""
        }
        let t: any;
        if (this.storeData["data"].warehouse.channel_id === null || this.storeData["data"].warehouse.channel_id === "") {
          t = "0"
        } else {
          t = this.storeData["data"].warehouse.channel_id
          // console.log("channel id : ", this.storeData["data"].warehouse.channel_id);
        }
        let data = {
          address: this.storeData["data"].warehouse.address,
          applicable_channel_id: "",
          applicable_country_id: this.storeData["data"].warehouse.country_id+"",
          channel_id: t,
          city: this.storeData["data"].warehouse.city,
          code: this.storeData["data"].warehouse.code,
          contact_person: this.contactperson,
          country_id: this.storeData["data"].warehouse.country_id,
          created: this.storeData["data"].warehouse.created,
          createdby: this.storeData["data"].warehouse.createdby,
          email: this.storeData["data"].warehouse.email,
          expected_delivery_time: this.deliverTimeModifier,
          fileUrl: "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/warehouselogo/200x200/" + this.storeData["data"].warehouse.warehouse_logo,
          id: this.storeData["data"].warehouse.id,
          invoice_id_format: this.storeData["data"].warehouse.invoice_id_format,
          ip_address: this.storeData["data"].warehouse.ip_address,
          isblocked: this.storeData["data"].warehouse.isblocked,
          isdeleted: this.storeData["data"].warehouse.isdeleted,
          latitude: this.storeData["data"].warehouse.latitude,
          longitude: this.storeData["data"].warehouse.longitude,
          manager_id: managerids.slice(0, -1),
          max_distance_sales: this.storeData["data"].warehouse.max_distance_sales,
          min_order_amount: this.storeData["data"].warehouse.min_order_amount,
          modified: this.datePipe.transform(new Date(), "yyyy-MM-dd"),
          name: this.storeData["data"].warehouse.name,
          order_id_format: this.storeData["data"].warehouse.order_id_format,
          payment_option: paymentids,
          phone: this.phoneNumber,
          product_stock_code: this.storeData["data"].warehouse.product_stock_code,
          shipping_id_format: this.storeData["data"].warehouse.shipping_id_format,
          state_id: this.storeData["data"].warehouse.state_id,
          state_name: this.storeData["data"].warehouse.state_name,
          store_category: warehouse_category,
          store_category_type: store_category_type,
          text_color: this.storeData["data"].warehouse.text_color,
          updatedby: this.storeData["data"].warehouse.updatedby,
          warehouseId: this.warehouse_id,
          warehouse_logo: this.storeData["data"].warehouse.warehouse_logo,
          website_id: this.website_id,
          zipcode: this.storeData["data"].warehouse.zipcode,
        }
        // console.log("data modal : ", data, " payment method : ", this.paymentmethod);
        this.apiService.updateData("warehouse/" + this.warehouse_id + "/", data).subscribe((data: any) => {
          // console.log("data");
          if (data.status === 1) {
            this.isSaved = true
            this.globalitem.showSuccess(data.message, "")
          } else {
            this.isSaved = false
            this.globalitem.showError("Something going wrong", "")
          }
        })
      } else {
        this.globalitem.showError("Phone number should be 10 to 12 characters", "")
      }
    })

  }
}
