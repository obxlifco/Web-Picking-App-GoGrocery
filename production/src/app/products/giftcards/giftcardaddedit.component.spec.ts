import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GiftcardaddeditComponent } from './giftcardaddedit.component';

describe('GiftcardaddeditComponent', () => {
  let component: GiftcardaddeditComponent;
  let fixture: ComponentFixture<GiftcardaddeditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GiftcardaddeditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GiftcardaddeditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
