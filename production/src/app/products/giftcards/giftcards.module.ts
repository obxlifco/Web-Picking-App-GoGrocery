import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { GiftcardsRoutingModule } from './giftcards-routing.module';
import { GiftcardsComponent } from './giftcards.component';
import { GiftcardaddeditComponent } from './giftcardaddedit.component';
import { BmscommonModule } from '../../bmscommon.module';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';

@NgModule({
  declarations: [
    GiftcardsComponent, 
    GiftcardaddeditComponent
  ],
  imports: [
    CommonModule,
    GiftcardsRoutingModule,
    BmscommonModule,
    OwlDateTimeModule, 
    OwlNativeDateTimeModule
  ]
})
export class GiftcardsModule { }
