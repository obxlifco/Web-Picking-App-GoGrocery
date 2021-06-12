import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SegmentRoutingModule } from './segment-routing.module';
import { BmscommonModule } from '../../bmscommon.module';
import { SegmentComponent } from './products.segment.component';

@NgModule({
  declarations: [
    SegmentComponent,
  ],
  imports: [
    CommonModule,
    SegmentRoutingModule,
    BmscommonModule,
  ]
})
export class SegmentModule { }
