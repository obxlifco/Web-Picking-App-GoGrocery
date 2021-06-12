import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoryBannerAddeditComponent } from './category-banner-addedit.component';

describe('CategoryBannerAddeditComponent', () => {
  let component: CategoryBannerAddeditComponent;
  let fixture: ComponentFixture<CategoryBannerAddeditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CategoryBannerAddeditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CategoryBannerAddeditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
