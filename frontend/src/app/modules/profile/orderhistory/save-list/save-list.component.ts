import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import {SavelistService} from '../../../../global/service/savelist.service';
import { GlobalService} from '../../../../global/service/app.global.service';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-save-list',
  templateUrl: './save-list.component.html',
  styleUrls: ['./save-list.component.css']
})
export class SaveListComponent implements OnInit {

  public saveListData:Array<any> = [];
  public isProcessing:boolean = true;

  constructor(private _saveListService:SavelistService,private _gs:GlobalService, @Inject(PLATFORM_ID) private platformId: Object
  ) { }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.getSaveListData();
    }


  }
  /**
   * Method for getting save list container
   * @access public
  */
  getSaveListData() {
    this._gs.showLoaderSpinner(true);
    this.isProcessing = true;
  	this._saveListService.getSaveList().subscribe(response => {
      this.isProcessing = false;
  		if(response && response['status'] == 1) {
        this.saveListData = response['data'];
        console.log(this.saveListData);

      }
      this._gs.showLoaderSpinner(false);

  	},
    error => {
      this._gs.showLoaderSpinner(false);
      this._gs.showToast("Something went wrong");
    }
    );
    () => {
     // this._gs.showLoaderSpinner(false);
    }
  }
  delete_item(itemId) {
    this._gs.showLoaderSpinner(true);
    this._saveListService.deleteSaveList(itemId).subscribe(response => {
      if(response && response['status'] == 200) {
        this.saveListData = response['data'];
      }

    },
    error => {
      this._gs.showLoaderSpinner(false);
      console.log("************** Delete error **************",error);

    },
    () => {
      this._gs.showLoaderSpinner(false);
    }
    )
  }
  navigate(navigationType) {

  }

}
