import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { ReceiptService, Receipt } from './receipt';

describe('ReceiptService', () => {
  let service: ReceiptService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ReceiptService, provideHttpClient(), provideHttpClientTesting()],
    });

    service = TestBed.inject(ReceiptService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    // Ensure that there are no outstanding requests
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should submit a receipt as FormData and trigger a refresh', () => {
    const mockReceipt: Receipt = {
      user_id: 'U1',
      merchant_name: 'Store A',
      total_amount: 10,
      purchase_date: '2024-01-01',
    };
    const mockFile = new File([''], 'receipt.jpg', { type: 'image/jpeg' });

    service.submitReceipt(mockReceipt, mockFile).subscribe();

    // 1. Handle the POST request
    const postReq = httpMock.expectOne('http://localhost:8000/api/v1/receipts');
    expect(postReq.request.method).toBe('POST');
    postReq.flush({ ...mockReceipt, id: 1, points_earned: 100 });

    // 2. Handle the follow-up GET request triggered by the 'tap' side effect
    const getReq = httpMock.expectOne('http://localhost:8000/api/v1/receipts');
    expect(getReq.request.method).toBe('GET');
    getReq.flush([]); // Flush an empty array to satisfy the request
  });
});
