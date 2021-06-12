import { TestBed } from '@angular/core/testing';

import { RelatedproductService } from './relatedproduct.service';

describe('RelatedproductService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: RelatedproductService = TestBed.get(RelatedproductService);
    expect(service).toBeTruthy();
  });
});
