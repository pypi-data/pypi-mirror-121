from azure_img_utils.azure_image import AzureImage
from pprint import pprint


img = AzureImage(
    container='images',
    storage_account='smarlowtesting',
    credentials_file='~/Documents/azure/updates_creds.json',
    resource_group='smarlow-testing'
)

offers = [
    'sles-15-sp3-chost-byos',
#    'sles-15-sp3-byos',
#    'sles-15-sp3-hpc',
#    'sles-15-sp3-hpc-byos',
#    'sles-15-sp3-basic',
#    'sles-sap-15-sp3',
#    'sles-sap-15-sp3-byos',
#    'manager-server-4-2-byos',
#    'manager-proxy-4-2-byos',
]

# print(img.get_offer_doc('sles-15-sp3-chost-byos', 'suse'))

# operation = img.publish_offer(
#     'sles-15-sp3-chost-byos',
#     'suse',
#     'smarlow@suse.com'
# )
# print(operation)

for offer in offers:
    if img.get_offer_status(offer, 'suse') == 'waitingForPublisherReview':
        operation = img.go_live_with_offer(offer, 'suse')
        print(f'Go Lived {offer}')
    elif img.get_offer_status(offer, 'suse') == 'succeeded':
        print(f'{offer} done!')
    elif img.get_offer_status(offer, 'suse') == 'running':
        print(f'{offer} chugging along')

# def wait_on_offer(
#         self,
#         offer_id: str,
#         publisher_id: str,
#         wait_time: int = 30
#     ):
#         """
#         Wait for the cloud partner operation to finish.

#         If the operation fails or is canceled an exception is raised.
#         """
#         while True:
#             status = self.get_offer_status(offer_id, publisher_id)

#             if status == 'waitingForPublisherReview':
#                 self.log.info(
#                     'Offer is waiting for publisher sign-off. '
#                     'Use go_live_with_offer to finish publishing.'
#                 )
#                 break
#             elif status == 'succeeded':
#                 self.log.info('Offer is live!')
#                 break
#             elif status == 'running':
#                 self.log.info('Offering running...')
#                 time.sleep(wait_time)
#             elif status in ('canceled', 'failed'):
#                 raise AzureImgUtilsException(
#                     f'Offer entered a failed state: {status}'
#                 )
#             else:
#                 raise AzureImgUtilsException(
#                     f'Offer entered an unknown state: {status}.'
#                 )
