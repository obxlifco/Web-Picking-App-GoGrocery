import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-editproductweight',
  templateUrl: './editproductweight.component.html',
  styleUrls: ['./editproductweight.component.scss']
})
export class EditproductweightComponent implements OnInit {

  editweightData:any=[]
  newprice:any
  newWeight:any
  notes:any
  constructor(
    public apiService :ApiService,
    public globalitem:GlobalitemService,
    public dialogRef: MatDialogRef<EditproductweightComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { 
      let tempdata:any=[]
      tempdata=data
      this.editweightData["data"]=tempdata.data
      console.log("edit weight data : ", data);
      
    }

  ngOnInit(): void {
    // this.editweightData['data']=[]
  }
  // products?.quantity,products?.product.weight,products?.product.uom.uom_full_name,products?.product_price,products?.product.name,products?.productean
  closeModal(){
this.dialogRef.close()
  }

  Apply(){
    // let data = {
    //   newprice: this.newprice,
    //   newweight: this.newWeight,
    //   notes:this.notes
    // }
    console.log("new weight : ",this.newWeight ,this.newprice,);
    

   let data={
      website_id:this.editweightData["data"].website_id,
      order_id: this.editweightData["data"].order_id,
      user_id: this.editweightData["data"].user_id,
      user_name: this.editweightData["data"].user_name,
      product_id:this.editweightData["data"].product.id,
      sku: this.editweightData["data"].product.sku,
      order_product_id: this.editweightData["data"].id,
      product_old_price: this.editweightData["data"].product_price,
      product_new_price:this.newprice,
      weight:this.newWeight,
      notes: ""
      }

      this.apiService.postData("picker-updatepicklistproductinfo/", data).subscribe((data: any[]) => {
        console.log("sendapproval : ",data);
        let tempdata:any=data
        // this.pickerProductList["data"] = data
        if(tempdata.status === 1){
          this.globalitem.showSuccess(tempdata.message,"Product Updated")
        }

      })
    this.dialogRef.close({ event: 'close', data: data });
  }
  totalweightPrice(totalweight :any,unitweight:any,unitprice:any,event:any){
    this.newprice = event.target.value/unitweight * unitprice
    console.log("price : ",event.target.value/unitweight * unitprice);
    console.log("unitweight : ",unitweight);
    console.log("unit price : ",unitprice);
    console.log("total weight : ",event.target.value);    
  }
}
