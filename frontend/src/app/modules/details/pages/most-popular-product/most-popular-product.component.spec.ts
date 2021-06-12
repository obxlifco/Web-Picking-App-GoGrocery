import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MostPopularProductComponent } from './most-popular-product.component';

describe('MostPopularProductComponent', () => {
  let component: MostPopularProductComponent;
  let fixture: ComponentFixture<MostPopularProductComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MostPopularProductComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MostPopularProductComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
