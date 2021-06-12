import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { GiftcardsComponent } from './giftcards.component';
import { GiftcardaddeditComponent } from './giftcardaddedit.component';

const routes: Routes = [
  { path: '', component: GiftcardsComponent },
  { path: 'add', component: GiftcardaddeditComponent },
  { path: 'edit/:id', component: GiftcardaddeditComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GiftcardsRoutingModule { }
