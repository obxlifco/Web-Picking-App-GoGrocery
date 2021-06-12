import { Component, OnInit } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { AreaService } from '../../operations/area/operation.area.service';
import * as XLSX from 'xlsx';
import { forEach } from '@angular/router/src/utils/collection';
@Component({
  selector: 'app-taxrateaddedit',
  templateUrl: 'templates/taxrateaddedit.component.html',
  providers: [AreaService],
  animations: [ AddEditTransition ],
  host: {
  '[@AddEditTransition]': ''
  },
})
export class TaxrateaddeditComponent implements OnInit {

  public ipaddress: any;
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;
    public country_list: any;
    public state_list: any;
    arrayBuffer:any;
    file:File;
    public zipcode_list=[];
    public pincodes_str:any;
	  public sample_xls: any;
    public pincode_state: any;
    constructor(
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        private _areaService: AreaService,
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {
		  this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/pincode_import_file.xls';
      let userData = this._cookieService.getObject('userData');
      this.userId = userData['uid'];
      this.getCountryList();
      this.tabIndex = +this._globalService.getCookie('active_tabs');
      this.parentId = this._globalService.getParentTab(this.tabIndex);
      this.sub = this._route.params.subscribe(params => {
          this.formModel.formId = +params['id']; // (+) converts string 'id' to a number
      });
      if (this.formModel.formId > 0) {
          this.global.getWebServiceData('view_taxrate','GET','',this.formModel.formId).subscribe(Response => {
              let data=Response.api_status;
              this.formModel.name = data.name;
              this.formModel.percentage = data.percentage;
              this.formModel.apply = data.apply;
              this.formModel.tax_type = data.tax_type;
              this.formModel.country_id = data.country.id;
              if (data.state_id != '') {
                let state = data.state_id;
                this.formModel.state_id = state.split(',').map(function(item) {
                    return parseInt(item, 10);
                });
              this.getState(this.formModel.country_id );
              } else {
                this.formModel.state_id = [];
              }
              this.formModel.zipcode = data.zipcode;
          }, err => {
              console.log(err)
          })
      }
      
  }

  addEdit(form: any) {
      setTimeout(() => {
          this._globalService.showLoaderSpinner(false);
      });
      if(this.formModel.zipcode){
        let zip_codes=[];
        zip_codes=this.formModel.zipcode.split(',');
        zip_codes.forEach((val)=>{
          //PIN CODE CHECKING
          if(val.length>8){
            this.pincode_state=1;
          }
          if(val >0){
            this.pincode_state=this.pincode_state;
          }else{
            this.pincode_state=1;
          }
        })
      }
      
      let data: any = {};
      data.website_id = this._globalService.getWebsiteId();
      data.name = this.formModel.name;
      data.apply = this.formModel.apply;
      data.percentage = this.formModel.percentage;
      data.tax_type = this.formModel.tax_type;
      data.country_id = this.formModel.country_id;
      if(this.formModel.state_id){
        let state_id=this.formModel.state_id.toString();
        data.state_id = state_id;
      }else{
        data.state_id = null;
      }
      data.zipcode = this.formModel.zipcode;
      if (this.formModel.formId > 0) {
          data.id = this.formModel.formId;
      }
      data={"value":data};
      if(this.pincode_state!=1){
        this.global.getWebServiceData('taxrate','POST',data,'').subscribe(res => { 
          if (res['status'] == '1') { // success response 
              this._globalService.showToast(res['message']);
              this._router.navigate(['/tax_rates/']);
          } else {
              this._globalService.showToast(res['message']);
          }
          setTimeout(() => {
              this._globalService.showLoaderSpinner(false);
          });
        }, err => {

        })
      }else{
        this._globalService.showToast('Please enter a zipcode');
        this.pincode_state=0;
      }
  }

  getCountryList() {
    this._areaService.loadCountry().subscribe(data => {
        //console.log(data)
        this.country_list = data.countrylist; // list of country list
    }, err => {}, function() { // call back function when exection is done
    })
  }

  getState(country_id: number) {
    this._areaService.loadStates(country_id).subscribe(data => {
        this.state_list = data.states;
    }, err => console.log(err), function() {});
  }

  //FILE UPLOAD START
  readfile(event) 
  {
    this.file= event.target.files[0]; 
    this.Upload();

  }

  Upload() {
    let fileReader = new FileReader();
      fileReader.onload = (e) => {
      this.arrayBuffer = fileReader.result;
      var data = new Uint8Array(this.arrayBuffer);
      var arr = new Array();
      for(var i = 0; i != data.length; ++i) arr[i] = String.fromCharCode(data[i]);
      var bstr = arr.join("");
      var workbook = XLSX.read(bstr, {type:"binary"});
      var first_sheet_name = workbook.SheetNames[0];
      var worksheet = workbook.Sheets[first_sheet_name];
      let row=XLSX.utils.sheet_to_json(worksheet,{raw:true});
      row.forEach((item,index) => {
        let pin=item['PINCODE'];
        this.zipcode_list.push(pin);
      })
      var arr = this.zipcode_list;
      var arr = arr.filter(function(item, pos){
        return arr.indexOf(item)== pos;
      });        
      this.pincodes_str = arr.toString();
      this.formModel.zipcode=this.pincodes_str;
      console.log(this.pincodes_str)
    }
    fileReader.readAsArrayBuffer(this.file);
  }
  //FILE ULOAD END
}
