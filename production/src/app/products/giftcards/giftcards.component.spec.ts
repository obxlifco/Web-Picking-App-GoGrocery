import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GiftcardsComponent } from './giftcards.component';

describe('GiftcardsComponent', () => {
  let component: GiftcardsComponent;
  let fixture: ComponentFixture<GiftcardsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GiftcardsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GiftcardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
