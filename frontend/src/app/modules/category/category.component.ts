import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Global,GlobalVariable} from '../../global/service/global';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.css']
})
export class CategoryComponent implements OnInit {

  constructor(private _route: ActivatedRoute, private global: Global, @Inject(PLATFORM_ID) private platformId: Object) { }
  public category_id: any;
  ngOnInit() {

    // get category id from the  url
    this._route.params.subscribe(params => {
      this.category_id = params['id'];

    });
    let first_filter = [];
    let second_filter = [];
    if (this.category_id) {
      first_filter.push({ "match": { "category_id.id": 22 } });
    }
    let must_filter = {};
    let aggr_filter = {};
    must_filter['must'] = first_filter;
    // must_filter['filter']=second_filter;

    let filter_set = {
      "query":
        { "bool": must_filter }
    }
    //   let elasticData = '{'+ 
    //    '"query": { '+
    //       '"bool": {'+
    //            "must":[
    //                 {"match": 
    //               {"category_id.id":22}
    //                } 
    //            ]
    //         }
    //     }
    // }';
    if (isPlatformBrowser(this.platformId)) {
      this.global.getListingData(filter_set).subscribe(data => {
        console.log(data);
      })
    }


  }

}
