import { TestBed } from '@angular/core/testing';

import { GlobalitemService } from './globalitem.service';

describe('GlobalitemService', () => {
  let service: GlobalitemService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GlobalitemService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
