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

  searchText = ''
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
    console.log("data : ",data);
    
    this.dialogRef.close({ event: 'close', data: data});
  }
  closeModal():void{
    this.dialogRef.close();
  }  
  getCategories(){
      let data={
        website_id:this.incomingModalData.data.website_id,
        warehouse_id:this.incomingModalData.data.warehouse_id,
        parent_id:this.incomingModalData.data.parent_id,
        isparent:0
      }
      console.log("going data : ",data);
      let temparray:any=[]
      
      this.apiService.postData(this.incomingModalData.data.URl, data).subscribe((data: any) => {
        console.log(data);
        this.categorylist["data"]=data
        if(this.incomingModalData.data.parent_id === null){
          for(let i=0;i<data.response?.length;i++){
            if(data.response[i]?.parent_id ===0){
              temparray.push(data.response[i])
            }
          }
          this.categorylist["data"]=temparray
          console.log("Parent Category ", this.categorylist["data"]);
          
        }else{
          for(let i=0;i<data?.response?.length;i++){
            if(data?.response[i]?.parent_id !==0){
              temparray.push(data.response[i])
            }
        }
        this.categorylist["data"]=temparray
        console.log("child Category ",temparray);
      }
      })  
    }
    
   
//   filterListCareUnit(val:any) {
//     console.log(val.key);
//     this.categorylist["data"] =  this.categorylist["data"].response.filter((unit:any) => unit.name.indexOf(val.key) > -1);
//  console.log("after filter : ",this.categorylist["data"]);
 
//   }


}
