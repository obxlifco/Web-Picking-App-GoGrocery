import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ApiService } from './../../services/api/api.service';
import { Component, Inject, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-productpromotionmodel',
  templateUrl: './productpromotionmodel.component.html',
  styleUrls: ['./productpromotionmodel.component.scss']
})
export class ProductpromotionmodelComponent implements OnInit {

  form: FormGroup;
  productdata :any= [];
  get productFormArray() {
    return this.form.controls.orders as FormArray;
  }
  incomingModalData:any=[]
  IsDataLoaded=false
  throttle = 300;
  scrollDistance = 2;
  scrollUpDistance = 1;
  productpage:any=1
  totalProductpage:any;
  constructor(private formBuilder: FormBuilder,public apiService :ApiService,public globalitem:GlobalitemService,
    public dialogRef: MatDialogRef<ProductpromotionmodelComponent>, @Inject(MAT_DIALOG_DATA) public data: DialogData) {
    this.form = this.formBuilder.group({
      orders: new FormArray([])
    });
    this.incomingModalData=data;
    console.log("incoming modal data : ",this.incomingModalData);
    this.getskuproductlist()
  }

  private addCheckboxes() {
    this.productdata.forEach(() => this.productFormArray.push(new FormControl(false)));
    console.log("data response : ", this.productFormArray);
  }

  submit() {
    const selectedproductsku = this.form.value.orders
      .map((checked:any, i:any) => checked ? this.productdata[i].sku : null)
      .filter((v: any) => v !== null);
       console.log(selectedproductsku);
    if(selectedproductsku.length !== 0){
  this.dialogRef.close({ event: 'close', data: selectedproductsku});
    }else{
      this.globalitem.showError("please select one product","")
    }
  }

  savedata(data:any){
    this.dialogRef.close({ event: 'close', data: data});
  }

  cancel(){
    this.dialogRef.close({ event: 'close'});
  }

  ngOnInit(): void {
  }
// getskuproductlist(){
//   let data={
//     data: {
//       query:{
//         bool:{
//           must:[
//             {match:
//               {'isdeleted':'n'}}]}},
//               from: 0,
//               size: 25  ,
//               sort: [{id: 'desc'}]},
//     table_name: "EngageboostProducts",
//     website_id: 1
//   }
//   this.apiService.postwithoutTokenData("search_elastic/", data).subscribe((data: any) => {
   
//     this.productdata=data?.hits?.hits
//     this.addCheckboxes();
//   })
// }

getskuproductlist(){
  let data = {
    website_id: this.incomingModalData.data.data.website_id,
    warehouse_id: this.incomingModalData.data.data.warehouse_id,
    page: this.productpage,
    search:this.incomingModalData.data.data.searchProductvalue,
    // per_page: 15,
    category_id: this.incomingModalData.data.categoryID,
    in_stock: 'y',
    has_price:'y',
    // product_stock_ids: 1
  }
  this.apiService.postData("picker-searchstock/", data).subscribe((data: any) => {
    console.log(data);
    if(this.productpage === 1){
      // this.pickerProductList["data"]=data.response
      this.totalProductpage=data.total_page
      this.productdata=data.response
    this.addCheckboxes();
    }else{
      // console.log("page n");
      this.productdata = [... this.productdata, ...data.response];
      this.addCheckboxes();
    }
    this.IsDataLoaded = false
  })
}

onScrollDown(ev:any) {
  console.log('scrolled!!',ev);
  this.productpage++;
  if(this.productpage <= this.totalProductpage){
    this.getskuproductlist()
  }else{
  }

}
}
