import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ApiService } from './../../services/api/api.service';
import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

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

  constructor(private formBuilder: FormBuilder,public apiService :ApiService,public globalitem:GlobalitemService,
    public dialogRef: MatDialogRef<ProductpromotionmodelComponent>,) {
    this.form = this.formBuilder.group({
      orders: new FormArray([])
    });

    this.getskuproductlist()
  }

  private addCheckboxes() {
    this.productdata.forEach(() => this.productFormArray.push(new FormControl(false)));
    console.log("data response : ", this.productFormArray);
  }

  submit() {
    const selectedproductsku = this.form.value.orders
      .map((checked:any, i:any) => checked ? this.productdata[i]._source.sku : null)
      .filter((v: any) => v !== null);
       console.log(selectedproductsku);
    if(selectedproductsku.length !== 0){
  this.dialogRef.close({ event: 'close', data: selectedproductsku});
    }else{
      this.globalitem.showError("please select one product","")
    }
  }
  cancel(){
    this.dialogRef.close({ event: 'close'});
  }

  ngOnInit(): void {
  }
getskuproductlist(){
  let data={
    data: {
      query:{
        bool:{
          must:[
            {match:
              {'isdeleted':'n'}}]}},
              from: 0,
              size: 25  ,
              sort: [{id: 'desc'}]},
    table_name: "EngageboostProducts",
    website_id: 1
  }
  this.apiService.postwithoutTokenData("search_elastic/", data).subscribe((data: any) => {
   
    this.productdata=data?.hits?.hits
    this.addCheckboxes();
  })
}
}
