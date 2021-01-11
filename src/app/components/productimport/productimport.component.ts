import { Component, ElementRef, Inject, isDevMode, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { NgxFileDropEntry, FileSystemFileEntry, FileSystemDirectoryEntry } from 'ngx-file-drop'
import { CommonfunctionService } from 'src/app/core/utilities/commonfunction.service';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import * as XLSX from 'xlsx'
import { DialogData } from '../addnewproduct/addnewproduct.component';
var $: any
@Component({
  selector: 'app-productimport',
  templateUrl: './productimport.component.html',
  styleUrls: ['./productimport.component.scss']
})
export class ProductimportComponent implements OnInit {

  @ViewChild("fileUpload", { static: false }) fileUpload: ElementRef | any;
  public files: NgxFileDropEntry[] = [];
  filename: any
  isFileDrop = true
  DBFields: any = []
  fileToUpload: any = File;
  title: any;
  file: any;
  arrayBuffer: any
  filelist: any
  userdata = {
    website_id: '1',
    userid: '',
    company_id: ''
  }
  subUrl: any
  usermodalData: any = []
  importproducts: any = []
  constructor(public commonfunc: CommonfunctionService, public apiService: ApiService, public globalitem: GlobalitemService,
    public dialogRef: MatDialogRef<ProductimportComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
    // console.log("Modal data : ", data);
    let tempdata: any = data
    this.usermodalData = tempdata.data
    this.userdata.website_id = tempdata.data.website_id
    this.userdata.company_id = tempdata.data.company_id
  }

  ngOnInit(): void {
  }

  closeModal() {
    this.dialogRef.close()
  }

  fileChange(event: any) {
    let fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      this.file = fileList[0];
    }
  }
  uploadFile() {
    let file: any = this.file
    // console.log("files data : ", this.files);
    let toastLabel: any;
    const formData = new FormData();
    formData.append('import_file', file);
    formData.append("website_id", this.userdata.website_id);
    formData.append("import_file_type", 'price');
    if (this.usermodalData.importsatus === "price") {
      this.subUrl = "import_price/"
      toastLabel = "Price"
    } else if (this.usermodalData.importsatus === "stock") {
      this.subUrl = "import_sheet/"
      formData.append("company_id", this.userdata.company_id);
      toastLabel = "Stock"
    }
    if (file !== undefined && this.commonfunc.isFileAllowed(this.files[0]?.relativePath)) {
      this.apiService.upload(this.subUrl, formData).subscribe((data: any) => {
        this.closeModal()
        this.globalitem.showSuccess(toastLabel + " will be updated soon", "")
      })
    } else {
      this.globalitem.showError("Please select Excel File", "")
    }
  }

  downloadsample() {
    let url: any = ''
    // console.log("modal status : ", this.usermodalData);
    if (this.usermodalData.importsatus === "price") {
      url = 'http://www.gogrocery.ae:8062/media/importfile/sample/price_import_sheet.xls'
    } else if (this.usermodalData.importsatus === "stock") {
      url = 'http://www.gogrocery.ae:8062/media/importfile/sample/stock_import.xls'
    }
    if (url) {
      this.commonfunc.generalDownloadfile(url)
    }
  }

  // drag and drop files 
  public dropped(files: NgxFileDropEntry[]) {
    this.isFileDrop = true
    this.files = files;
    for (const droppedFile of files) {
      // Is it a file?
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file1: File) => {
          // Here you can access the real file
          this.file = file1
          // console.log(droppedFile.relativePath, file1);
        });
      } else {
        // It was a directory (empty directories are added, otherwise only files)
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
        // console.log(droppedFile.relativePath, fileEntry);
      }
    }
  }

  public fileOver(event: any) {
    this.isFileDrop = false
    // console.log(event);
  }

  public fileLeave(event: any) {
    this.isFileDrop = true
    // console.log(event);
  }
}


