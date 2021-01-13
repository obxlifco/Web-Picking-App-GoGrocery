import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ModalService } from 'src/app/services/modal/modal.service';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-editprice',
  templateUrl: './editprice.component.html',
  styleUrls: ['./editprice.component.scss']
})
export class EditpriceComponent implements OnInit {
  price:any='';
  modaldata:any=[]
  constructor(public modalservice : ModalService,
    public globalitem:GlobalitemService,
    public apiservice : ApiService,
    public dialogRef: MatDialogRef<EditpriceComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
    ) {
      // console.log("incoming modal data : ",data);
      
      this.modaldata=data
     }

  ngOnInit(): void {
  }

  closeModal(){
    this.dialogRef.close()    
  }
  updatePrice(){
    // let data={
    //   website_id:this.modaldata.data.website_id,
    //   order_id:this.modaldata.data.order_id,
    //   user_id:this.modaldata.data.user_id,
    //   order_amount: this.modaldata.data.order_amount,
    //   updated_order_amount: this.price
    // }

    let data=this.getobjectData()
    
    if(this.modaldata.data.pricestatus === 'unitprice'){
      let pricedata={
        user_name: this.modaldata.data.user_name,
        product_id:this.modaldata.data.productinfo.product.id,
        sku: this.modaldata.data.productinfo.product.sku,
        order_product_id: this.modaldata.data.productinfo.id,
        product_old_price: this.modaldata.data.order_amount,
        product_new_price: this.price,
        weight:this.modaldata.data.unitweight,
        notes:"qwewqewq"
      }
      Object.assign(data,pricedata)
      // console.log("object data is ",data);
      
    }else{
      let detailpricedata={
        order_amount: this.modaldata.data.order_amount,
        updated_order_amount: this.price
      }
      Object.assign(data,detailpricedata)
    }
    if(this.price.length !== 0 && this.price !== '0'){
    this.apiservice.postData(this.modaldata.data.URL, data).subscribe((data: any) => 
    {
      if(data.status === 1){
        this.globalitem.showSuccess("Price updated successfully ","Price Updated")
        this.dialogRef.close({ event: 'close', price: this.price});
      }else{
        this.globalitem.showError(data.message,"")
        // this.dialogRef.close({ event: 'close', billnumber: this.bill_number});
      }
      
    })
  }else{
    this.globalitem.showError("First you need to Enter Bill Number","Bill Number")
  }
  }

  getobjectData(){
    let data={
      website_id:this.modaldata.data.website_id,
      order_id:this.modaldata.data.order_id,
      user_id:this.modaldata.data.user_id,
    }
    return data
  }
}
