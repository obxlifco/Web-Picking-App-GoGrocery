import { Component, Inject, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { of } from 'rxjs';
import { debounceTime, startWith, switchMap } from 'rxjs/operators';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { DialogData } from '../addnewproduct/addnewproduct.component';

@Component({
  selector: 'app-addproductcategory',
  templateUrl: './addproductcategory.component.html',
  styleUrls: ['./addproductcategory.component.scss']
})
export class AddproductcategoryComponent implements OnInit {

  search = new FormControl();
  searchControl = new FormControl();
  categoryData={
    categoryurl:'',
    website_id:'',
    parent_id:''
  }
  incomingModalData:any=[]
  categorylist:any=[]
  constructor(
    public apiService: ApiService,
    public globalitem: GlobalitemService,
    public dialogRef: MatDialogRef<AddproductcategoryComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
      console.log("modal incoming data : ",data);
      this.incomingModalData=data
      // this.categorylist["data"]=[]
      this.getCategories()
     }

    //  $search = this.search.valueChanges.pipe(
    //   startWith(null),
    //   debounceTime(200),
    //   switchMap((res: string) => {
    //     if (!res) return of(this.categorylist["data"]?.response);
    //     res = res.toLowerCase();
    //     return of(
    //       this.categorylist["data"]?.response.filter((x: string) => x.toLowerCase().indexOf(res) >= 0)
    //     );
    //   })
    // );

    // selectionChange(option: any) {
    //   let value = this.searchControl.value || [];
    //   if (option.selected) value.push(option.value);
    //   else value = value.filter((x: any) => x != option.value);
    //   this.searchControl.setValue(value);
    // }

  ngOnInit(): void {
  }

  listItem(data:any){
    this.dialogRef.close({ event: 'close', data: data});
  }
  closeModal():void{
    this.dialogRef.close();
  }  
  getCategories(){
    let data={
      website_id:this.incomingModalData.data.website_id,
      warehouse_id:this.incomingModalData.data.warehouse_id,
      parent_id:this.incomingModalData.parent_id,
    }
    console.log("going data : ",data);
    
    this.apiService.postData(this.incomingModalData.data.categoryURl, data).subscribe((data: any[]) => {
      console.log(data);
      this.categorylist["data"]=data
    })
  }
}
