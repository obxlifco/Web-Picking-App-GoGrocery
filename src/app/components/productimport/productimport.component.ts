import { HttpErrorResponse, HttpEventType } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { CommonfunctionService } from 'src/app/core/utilities/commonfunction.service';
import { ApiService } from 'src/app/services/api/api.service';
import * as XLSX from 'xlsx'
@Component({
  selector: 'app-productimport',
  templateUrl: './productimport.component.html',
  styleUrls: ['./productimport.component.scss']
})
export class ProductimportComponent implements OnInit {

  @ViewChild("fileUpload", {static: false}) fileUpload: ElementRef |any ;
  files:any = [];
  filename:any
  DBFields:any=[]
  
  title:any;
  file:any=File;
  arrayBuffer:any
  filelist:any
  constructor(public commonfunc : CommonfunctionService,public apiService:ApiService,
    public dialogRef: MatDialogRef<ProductimportComponent>) {
     
     }

  ngOnInit(): void {
  }

  uploadListener($event: any): void {  
  
    let text = [];  
    let files = $event.srcElement.files;  
    console.log("file is : ",$event);
    // this.commonfunc.uploadListener($event)
    // setTimeout(()=>{
    //   this.commonfunc.getRecord().then((res: any)=>{
    //     console.log("respone of records : ",res);
    //     this.importProducts($event,res)
    //   })
    // },200)
   
   
  this.file= $event.target.files[0];     
  let fileReader = new FileReader();    
  fileReader.readAsArrayBuffer(this.file);     
  fileReader.onload = (e) => {    
      this.arrayBuffer = fileReader.result;    
      var data = new Uint8Array(this.arrayBuffer);    
      var arr = new Array();    
      for(var i = 0; i != data.length; ++i) arr[i] = String.fromCharCode(data[i]);    
      var bstr = arr.join("");    
      var workbook = XLSX.read(bstr, {type:"binary"});    
      var first_sheet_name = workbook.SheetNames[0];    
      var worksheet = workbook.Sheets[first_sheet_name];    
      console.log("json Data : ",XLSX.utils.sheet_to_json(worksheet,{raw:true}));    
      // console.log("worksheet : ",worksheet);    
        var arraylist = XLSX.utils.sheet_to_json(worksheet,{raw:true});     
            this.filelist = [];    
            console.log(this.filelist)   
            // this.importProducts($event,XLSX.utils.sheet_to_json(worksheet,{raw:true}))    
}  
   
    
    
  }
  closeModal(){
    this.dialogRef.close()
  }

  importProducts(event:any,objectData:any){
    let files = event.srcElement;  
  
    const file = event.target.files[0];
    let product='product'
    let data={
      import_file: (objectData),
      website_id: 1,
      with_category: 0,
      import_file_type: product,
      
    }
    this.apiService.postbulkData("import_file_products/", data,file,event.target).subscribe((data: any[]) => {
      console.log(data);

    })
  }

  onClick() {
        const fileUpload :any = this.fileUpload.nativeElement;fileUpload.onchange = () => {
        for (let index = 0; index < fileUpload.files.length; index++)
        {
         const file = fileUpload.files[index];
         this.files.push({ data: file, inProgress: false, progress: 0});
        }
          this.uploadFile(this.files);
        };
        fileUpload.click();
    }
  uploadFile(file:any) {
    console.log("files is : ",file);
    
        const formData = new FormData();  
        formData.append('import_file', file[0].data);  
        formData.append("website_id", '1');
        formData.append("with_category", '0');
        formData.append("import_file_type", 'product');
        file[0].inProgress = true;
        this.apiService.upload('import_file_products/',formData).subscribe((data: any) => {
            console.log("response : ",data);
            this.filename=data.filename;
                this.DBFields=data.db_fields
                this.savefileData()
          })

        // this.apiService.upload('import_file_products/',formData).pipe(
        //   map((event:any) => {
        //     console.log("event value : ",event);
        //     this.filename=event.body.filename;
        //     this.DBFields=event.body.db_fields
        //     this.savefileData()
        //   }),  
        //   catchError((error: HttpErrorResponse) => {
        //     console.log("failed");
            
        //     file[0].inProgress = false;
        //     return of(`Upload failed: ${file[0].data.name}`);
        //   })).subscribe((event: any) => {
        //     if (typeof (event) === 'object') {
        //       console.log(event.body);
        //     }  
        //   });  
      }


      savefileData(){
        let mapProductlist :any=[]
        console.log("db fileds : ",this.DBFields);
        for(let i=0;i<this.DBFields.length;i++){
        
          this.DBFields[i].field_label={
            field_name: this.DBFields[i].model_field_value,
            id:0
          }

        // let  plist = [
        //   this.DBFields[i].field_label={
        //     field_name: this.DBFields[i].model_field_value,
        //     id:0
        //   },
        //     ];
        }
        console.log("db fileds : ",this.DBFields);
        let data={
          category_id: 511,
          filename: this.filename,
          map_fields: mapProductlist,
          website_id: 1,
          with_category: 0
        }
        console.log("mapProductlist : ",mapProductlist);
        
      }
}
