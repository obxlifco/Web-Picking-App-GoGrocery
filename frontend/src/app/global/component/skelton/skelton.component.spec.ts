import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SkeltonComponent } from './skelton.component';

describe('SkeltonComponent', () => {
  let component: SkeltonComponent;
  let fixture: ComponentFixture<SkeltonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SkeltonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SkeltonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
