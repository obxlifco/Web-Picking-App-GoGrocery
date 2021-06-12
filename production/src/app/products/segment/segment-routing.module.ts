import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SegmentComponent } from './products.segment.component';
const routes: Routes = [
  { path: '', component: SegmentComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SegmentRoutingModule { }
