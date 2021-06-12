import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CategoryBannerRoutingModule } from './category-banner-routing.module';
import { CategoryBannerAddeditComponent, linkBannerComponent, CatBannerProductListComponent, CatBannerCategoryListComponent } from './category-banner-addedit.component';
import { CategoryBannerComponent } from './category-banner.component';
import { BmscommonModule } from '../../bmscommon.module';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  declarations: [
      CategoryBannerComponent,
      CategoryBannerAddeditComponent,
      linkBannerComponent,
      CatBannerProductListComponent,
      CatBannerCategoryListComponent
    ],
  imports: [
    CommonModule,
    CategoryBannerRoutingModule,
    BmscommonModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    NgSelectModule,
  ],
  entryComponents:[
    linkBannerComponent,
    CatBannerProductListComponent,
    CatBannerCategoryListComponent
  ]
})
export class CategoryBannerModule { }
