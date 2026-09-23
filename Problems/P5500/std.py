def merge(nums1, m, nums2, n):
    # 从后往前双指针合并，避免覆盖 nums1 前部有效元素
    i, j, k = m - 1, n - 1, m + n - 1
    while i >= 0 and j >= 0:
        if nums1[i] >= nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1


def main():
    m, n = map(int, input().split())
    nums1 = list(map(int, input().split()))
    if n > 0:
        nums2 = list(map(int, input().split()))
    else:
        nums2 = []
    merge(nums1, m, nums2, n)
    print(" ".join(str(x) for x in nums1))


if __name__ == "__main__":
    main()
